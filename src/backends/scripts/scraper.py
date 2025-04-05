import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def scrape_website(url: str) -> str:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
            
            page.goto(url, wait_until="load", timeout=60000)

            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                print("Warning: Network idle not reached within timeout, proceeding...")

            html = page.content()
            browser.close()

            soup = BeautifulSoup(html, "html.parser")

            # Include <span> in the list of elements to search for
            elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span'])
            sections = []
            current_section = None
            section_count = 0

            for element in elements:
                if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    if current_section:
                        sections.append(current_section)
                    section_count += 1
                    current_section = {
                        "id": f"section_{section_count}",
                        "content": element.get_text(" ", strip=True),
                        "links": [{"href": a.get("href"), "content": a.get_text(strip=True)} for a in element.find_all("a", href=True)]
                    }
                elif element.name in ["p", "span"]:
                    if current_section is None:
                        section_count += 1
                        current_section = {
                            "id": f"section_{section_count}",
                            "content": "",
                            "links": []
                        }
                    current_section["content"] += " " + element.get_text(" ", strip=True)
                    current_section["links"].extend(
                        [{"href": a.get("href"), "content": a.get_text(strip=True)} for a in element.find_all("a", href=True)]
                    )

            if current_section:
                sections.append(current_section)

            return json.dumps(sections, indent=4)
    except Exception as e:
        return json.dumps({"error": str(e)})
