from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
import diskcache as dc
from functools import lru_cache
import subprocess

# Import scripts
from scripts.seo import analyze_seo, get_keyword_suggestions, optimize_metadata
from scripts.scraper import scrape_website
from scripts.rag_utils import vec_store, retrieval
from scripts.content_update import process_update
from scripts.content_addition import process_add
from scripts.error_link import process_links

# Import database blueprints
from database.user_data import users_bp
from database.api_keys_data import api_keys_bp
from database.websites_data import websites_bp

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Register database blueprints
app.register_blueprint(users_bp)
app.register_blueprint(api_keys_bp)
app.register_blueprint(websites_bp)

# Persistent cache
cache = dc.Cache("cache_dir")  # Disk-based cache
CACHE_EXPIRY_HOURS = 1  # Cache expiration time in hours


def is_cache_valid(timestamp):
    """Check if cache data is still valid."""
    return time.time() - timestamp < CACHE_EXPIRY_HOURS * 3600

@app.route('/scrape', methods=["GET"])
def scrape():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    # Check if data is cached
    if url in cache and is_cache_valid(cache[url]['timestamp']):
        return jsonify(cache[url]['data'])

    result = scrape_website(url)
    try:
        data = json.loads(result)
        cache[url] = {"data": data, "timestamp": time.time()}  # Store result in cache
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update', methods=["GET"])
def update():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        scraped = scrape_website(url)
        if isinstance(scraped, str):
            scraped = json.loads(scraped)

        # Check cache
        cache_key = f"update_{url}"
        if cache_key in cache and is_cache_valid(cache[cache_key]['timestamp']):
            return jsonify(cache[cache_key]['data'])

        suggestions = process_update(scraped)
        cache[cache_key] = {"data": suggestions, "timestamp": time.time()}
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

        # Check cache
        cache_key = f"add_{url}"
        if cache_key in cache and is_cache_valid(cache[cache_key]['timestamp']):
            return jsonify(cache[cache_key]['data'])

        suggestions = process_add(scraped)
        cache[cache_key] = {"data": suggestions, "timestamp": time.time()}
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

        # Check cache
        cache_key = f"errorlink_{url}"
        if cache_key in cache and is_cache_valid(cache[cache_key]['timestamp']):
            return jsonify(cache[cache_key]['data'])

        broken_links = process_links(scraped_data, base_url=url)
        cache[cache_key] = {"data": broken_links, "timestamp": time.time()}
        return jsonify({"broken_links": broken_links})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/seo', methods=["GET"])
def seo():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        cache_key = f"seo_{url}"
        if cache_key in cache and is_cache_valid(cache[cache_key]['timestamp']):
            return jsonify(cache[cache_key]['data'])

        seo_report = analyze_seo(url)
        keyword_data = get_keyword_suggestions(url)

        current_html = "<html><head><title>Example</title></head><body></body></html>"
        optimized_html = optimize_metadata(current_html)

        result = {
            "seo_report": seo_report,
            "keyword_data": keyword_data,
            "optimized_html": optimized_html,
        }

        cache[cache_key] = {"data": result, "timestamp": time.time()}
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
    cache.clear()  # Clear all cache entries
    return jsonify({"message": "Cache cleared successfully"})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)



#adding random stuff lol just to check