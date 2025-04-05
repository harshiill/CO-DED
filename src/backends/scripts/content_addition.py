import json
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from scripts.rag_utils import vec_store, retrieval

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)



def gen_prompt(text, links, context):
    link_str = "\n".join([f"- {l['content']} ({l['href']})" for l in links]) if links else "None"
    return f"""You are a helpful assistant that improves the reliability and authenticity of web content.

    Context from related documents:
    \"\"\"{context}\"\"\"

    Current content:
    \"\"\"{text}\"\"\"

    Links currently in the content:
    {link_str}

    Suggest additional information that could improve trust, clarity, and authenticity of the above content. 
    Focus on data, citations, expert opinions, historical background, or any other useful enhancements.

    Please respond ONLY in the following JSON format:
    {{
        "suggestions": [
            {{
                "addition": "A sentence or paragraph suggestion.",
                "reason": "Why this improves reliability or authenticity."
            }},
            ...
        ]
    }}
    """



def query_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        content = response.text.strip()

        json_matches = re.findall(r'{[\s\S]*?}', content)
        for match in json_matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
        return {
            "outdated": False,
            "error": "No valid JSON object found in Gemini response"
        }
        
    except Exception as e:
        return json.dumps({
            "outdated": False,
            "error": str(e)
        })


def process_add(sdata):
    index, embeddings, texts = vec_store(sdata)
    result = []


    for item in sdata:
        try:
            context = retrieval(index, embeddings, texts, item["content"], top=3)
            prompt = gen_prompt(item["content"], item.get("links", []), context)
            sugesstion_json = query_gemini(prompt)
            sugesstion = sugesstion_json
        except Exception as e:
            sugesstion = {
                "outdated": False,
                "error": str(e)
            }

        result.append({
            "id": item["id"],
            "orignal_content": item["content"],
            "links": item.get("links", []),
            "analysis": sugesstion
        })
    return result



def main():
    input = "testscrape.json"
    output= f"sugesstion_output.json"

    sdata = load_data(input)
    sugesstions = process_add(sdata)

if __name__ == "__main__":
    main()