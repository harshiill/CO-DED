import os
import json
import time
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

# Import scripts
from scripts.seo import analyze_seo, get_keyword_suggestions, optimize_metadata
from scripts.scraper import scrape_website
from scripts.rag_utils import vec_store, retrieval
from scripts.content_update import process_update
from scripts.content_addition import process_add
from scripts.error_link import process_links

from database.websites_data import websites_bp 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.register_blueprint(websites_bp)

from database.conn import db
websites_collection = db["websites"]

CACHE_EXPIRY_HOURS = 1  # 1 hour

def is_cache_valid(created_at):
    return (datetime.now(datetime.timezone.utc) - created_at) < timedelta(hours=CACHE_EXPIRY_HOURS)

@app.route('/scraped-data', methods=["GET"])
def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    website_doc = websites_collection.find_one({"url": url})
    if website_doc and "created_at" in website_doc:
        if is_cache_valid(website_doc["created_at"]):
            # Return cached scraped data if available.
            return jsonify(website_doc.get("scrape_data", {}))
    
    # If not cached or expired, perform scraping.
    result = scrape_website(url)
    try:
        data = json.loads(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    websites_collection.update_one(
        {"url": url},
        {"$set": {
            "scrape_data": data,
            "created_at": datetime.utcnow()
        }},
        upsert=True
    )
    return jsonify(data)

@app.route('/update', methods=["GET"])
def update():
    url = request.args.get("url")
    if not url:
         return jsonify({"error": "URL parameter is required"}), 400
    try:
        scraped = scrape_website(url)
        if isinstance(scraped, str):
            scraped = json.loads(scraped)

        suggestions = process_update(scraped)
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/add', methods=["GET"])
def add():
    url = request.args.get("url")
    if not url:
         return jsonify({"error": "URL parameter is required"}), 400
    try:
        scraped = scrape_website(url)
        if isinstance(scraped, str):
            scraped = json.loads(scraped)

        suggestions = process_add(scraped)
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/errorlink', methods=["GET"])
def errorlink():
    url = request.args.get("url")
    if not url:
         return jsonify({"error": "URL parameter is required"}), 400
    try:
        scraped = scrape_website(url)
        try:
            scraped_data = json.loads(scraped)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON response from scraper"}), 500
        
        broken_links = process_links(scraped_data, base_url=url)
        return jsonify({"broken_links": broken_links})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/seo', methods=["GET"])
def seo():
    url = request.args.get("url")
    if not url:
         return jsonify({"error": "URL parameter is required"}), 400
    try:
         seo_report = analyze_seo(url)
         keyword_data = get_keyword_suggestions(url)
         current_html = "<html><head><title>Example</title></head><body></body></html>"
         optimized_html = optimize_metadata(current_html)
         result = {
             "seo_report": seo_report,
             "keyword_data": keyword_data,
             "optimized_html": optimized_html,
         }
         return jsonify(result)
    except Exception as e:
         return jsonify({"error": str(e)}), 500

@app.route('/setup-aider', methods=["POST"])
def setup_aider():
    data = request.get_json()
    working_dir = data.get("workingDir")

    if not working_dir:
        return jsonify({"error": "Working directory is required."}), 400

    try:
        command = (
            f'cd "{working_dir}" && '
            'export GROQ_API_KEY=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 && '
            'echo "yes" | aider --model groq/llama3-70b-8192 --no-show-model-warnings '
            '--message "Update the navbar so that it looks more beautiful and elegant and do it according to yourself, make sure you only change one file tho."'
        )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True
        )

        if result.returncode != 0:
            return jsonify({"error": result.stderr}), 500

        return jsonify({"stdout": result.stdout})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear-cache', methods=["DELETE"])
def clear_cache():
    websites_collection.update_many({}, {"$unset": {"scrape_data": ""}})
    return jsonify({"message": "Cache cleared successfully"})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
