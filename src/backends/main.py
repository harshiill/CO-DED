import os
import signal
import sys
import json
import asyncio
import threading
import subprocess
from datetime import datetime, timedelta
from typing import TypedDict
from fastapi import FastAPI, Body, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uvicorn import Config, Server

# Import scripts from your existing project
from scripts.scraper import scrape_website
from scripts.llm_utils import vec_store, retrieval
from scripts.content_update import process_update
from scripts.error_link import process_links
from scripts.seo import analyze_seo, get_keyword_suggestions, optimize_metadata
from inference import infer_text_api  # Ensure this module is correctly imported

PORT_API = 8008
CACHE_FILE = "scraped_cache.json"
CACHE_EXPIRY_HOURS = 1

server_instance = None  # Global reference to the Uvicorn server instance

app = FastAPI(
    title="API Server",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### API ENDPOINTS ###

@app.get("/v1/connect")
def connect_to_api_server():
    print("[server] Connecting to server...", flush=True)
    host = f"http://localhost:{PORT_API}"
    return {
        "message": f"Connected to API server on port {PORT_API}. Refer to '{host}/docs' for API docs.",
        "data": {
            "port": PORT_API,
            "pid": os.getpid(),
            "host": host,
        },
    }

class T_Query(TypedDict):
    prompt: str

@app.post("/v1/completions")
def llm_completion(payload: T_Query = Body(...)):
    return infer_text_api.completions(payload)

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def save_cache(data):
    with open(CACHE_FILE, "w") as file:
        json.dump(data, file, indent=4)

async def get_scraped_data(url: str):
    cache = load_cache()
    if url in cache:
        cached_time = datetime.fromisoformat(cache[url]["timestamp"])
        if datetime.now() - cached_time < timedelta(hours=CACHE_EXPIRY_HOURS):
            return cache[url]["data"]

    result = await scrape_website(url)
    try:
        data = json.loads(result)
    except Exception as e:
        data = {"error": str(e)}

    cache[url] = {"data": data, "timestamp": datetime.now().isoformat()}
    save_cache(cache)
    return data

@app.get("/scraped-data")
async def scrape(url: str = Query(..., description="Website URL to scrape")):
    data = await get_scraped_data(url)
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    return data

@app.get("/update-content")
async def update(url: str = Query(..., description="Website URL to update content")):
    scraped = await get_scraped_data(url)
    if "error" in scraped:
        raise HTTPException(status_code=500, detail=scraped["error"])
    suggestions = process_update(scraped)
    return suggestions

@app.get("/errorlink")
async def errorlink(url: str = Query(..., description="Website URL to check for broken links")):
    scraped = await get_scraped_data(url)
    if "error" in scraped:
        raise HTTPException(status_code=500, detail=scraped["error"])
    broken_links = process_links(scraped, base_url=url)
    return {"broken_links": broken_links}

@app.get("/seo")
async def seo(url: str = Query(..., description="Website URL for SEO analysis")):
    try:
        seo_report = analyze_seo(url)
        keyword_data = get_keyword_suggestions(url)
        current_html = "<html><head><title>Example</title></head><body></body></html>"
        optimized_html = optimize_metadata(current_html)
        return {
            "seo_report": seo_report,
            "keyword_data": keyword_data,
            "optimized_html": optimized_html,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AiderSetupRequest(BaseModel):
    workingDir: str

@app.post("/setup-aider")
async def setup_aider(request_data: AiderSetupRequest):
    working_dir = request_data.workingDir

    if not working_dir:
        raise HTTPException(status_code=400, detail="Working directory is required.")

    try:
        command = (
            f'cd "{working_dir}" && '
            'export GROQ_API_KEY=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 && '
            'echo "yes" | aider --model groq/llama3-70b-8192 --no-show-model-warnings '
            '--message "Update the navbar so that it looks more beautiful and elegant and do it according to yourself, make sure you only change one file tho."'
        )

        result = subprocess.run(
            command, capture_output=True, text=True, shell=True
        )

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        return {"stdout": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear-cache")
async def clear_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
    return {"message": "Cache cleared successfully"}

### PROGRAMMATIC SERVER START/STOP ###

def kill_process():
    os.kill(os.getpid(), signal.SIGINT)  # Forcefully stops this script

def start_api_server(**kwargs):
    global server_instance
    port = kwargs.get("port", PORT_API)
    try:
        if server_instance is None:
            print("[sidecar] Starting API server...", flush=True)
            config = Config(app, host="0.0.0.0", port=port, log_level="info")
            server_instance = Server(config)
            asyncio.run(server_instance.serve())  # Start ASGI server
        else:
            print("[sidecar] Server is already running.", flush=True)
    except Exception as e:
        print(f"[sidecar] Error starting API server: {e}", flush=True)

def stdin_loop():
    print("[sidecar] Waiting for commands...", flush=True)
    while True:
        user_input = sys.stdin.readline().strip()
        match user_input:
            case "sidecar shutdown":
                print("[sidecar] Received 'sidecar shutdown' command.", flush=True)
                kill_process()
            case _:
                print(f"[sidecar] Invalid command [{user_input}]. Try again.", flush=True)

def start_input_thread():
    try:
        input_thread = threading.Thread(target=stdin_loop)
        input_thread.daemon = True  # So it exits when the main program exits
        input_thread.start()
    except:
        print("[sidecar] Failed to start input handler.", flush=True)

if __name__ == "__main__":
    start_input_thread()
    start_api_server()
