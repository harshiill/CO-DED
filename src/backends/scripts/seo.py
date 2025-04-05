import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key="GOOGLE_API_KEY")
LIGHTHOUSE_API_URL = os.getenv("LIGHTHOUSE_API_URL")

def analyze_seo(url: str) -> dict:
    """Analyze page performance and SEO metrics using Lighthouse API."""
    response = requests.get(f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?key={LIGHTHOUSE_API_URL}&url={url}")
    return response.json() if response.status_code == 200 else {"error": "Failed to retrieve SEO data"}

def get_keyword_suggestions(query: str) -> dict:
    """
    Fetch keyword suggestions using SerpApi.
    Instead of using a dedicated "suggestions" key, this function extracts the
    snippet_highlighted_words from the response, ensuring the returned words are unique.
    """
    serp_api_key = os.getenv("SERP_API_KEY")
    params = {
        "engine": "google", 
        "q": query,
        "api_key": serp_api_key,
    }
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        data = response.json()
        unique_words = set()

        # Extract from organic_results if available
        if "organic_results" in data:
            for result in data["organic_results"]:
                if "snippet_highlighted_words" in result:
                    for word in result["snippet_highlighted_words"]:
                        unique_words.add(word)

        # Fallback: Extract from related_questions if no keywords were found
        if not unique_words and "related_questions" in data:
            for item in data["related_questions"]:
                if "snippet_highlighted_words" in item:
                    for word in item["snippet_highlighted_words"]:
                        unique_words.add(word)

        return {"keywords": list(unique_words), "status": "success"}
    return {"error": "Failed to retrieve keyword suggestions", "status": "failure"}

def optimize_metadata(html: str) -> str:
    """Optimize HTML metadata using Gemini API."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Optimize the following HTML metadata for SEO:\n\n{html}"

    try:
        response = model.generate_content([prompt])
        return response.text.strip()
    except Exception as e:
        return f"Gemini API error: {e}"
