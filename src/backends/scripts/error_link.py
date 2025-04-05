import os
import json
import requests
from urllib.parse import urlparse, urljoin
import google.generativeai as genai
from dotenv import load_dotenv
from scripts.rag_utils import vec_store, retrieval

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def check_broken_links(scraped_data, base_url):
    if isinstance(scraped_data, str):
        scraped_data = json.loads(scraped_data)
    
    broken_links = []
    
    for section in scraped_data:
        if not isinstance(section, dict):  
            continue  # Skip invalid sections

        for link in section.get("links", []):
            if not isinstance(link, dict):  
                continue  # Skip invalid links

            href = link.get("href")
            if not href:
                continue  # Skip empty links

            # Convert relative URLs to absolute URLs
            if base_url and not urlparse(href).netloc:
                href = urljoin(base_url, href)

            try:
                response = requests.head(href, allow_redirects=True, timeout=5)
                if response.status_code >= 400:
                    broken_links.append(href)
            except requests.RequestException:
                broken_links.append(href)

    print(broken_links)

def gen_prompt(broken_links, context="Wikipedia or general knowledge"):
    links_formatted = "\n".join([f"- {link['content']}: {link['href']}" for link in broken_links])
    
    prompt = f"""
        You are a helpful assistant that suggests correct or updated URLs for broken web links.

        Contextual knowledge: {context}

        Broken links detected:
        {links_formatted}

        Please suggest a possible replacement for each link (if available) based on the link text and known public resources.

        Return ONLY in the following JSON format:
        [
        {{
            "original": "broken URL",
            "text": "link text",
            "suggested_replacement": "suggested updated URL or explanation"
        }}
        ]
        """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        content = response.text.strip()

        json_matches = json.loads(content)
        return json_matches

    except Exception as e:
        return [{"error": str(e)}]


def process_links(sdata, base_url=None):
    index, embeddings, texts = vec_store(sdata)
    result = []

    for item in sdata:
        try:
            broken_links = check_broken_links([item], base_url=base_url)
            context = retrieval(index, embeddings, texts, item["content"], top=3)
            if broken_links:
                suggestions = gen_prompt(broken_links, context)
            else:
                suggestions = []

            result.append({
                "id": item.get("id"),
                "original_links": item.get("links", []),
                "broken_links": broken_links,
                "context_used": context,
                "suggestions": suggestions
            })

        except Exception as e:
            result.append({
                "id": item.get("id"),
                "error": str(e)
            })

    return result


    return broken_links
