import os, json, re, time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3.5-flash"   # use the model name that worked for you earlier

def ask(prompt, system="", max_tokens=2000):
    for attempt in range(3):
        try:
            r = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system or None,
                    max_output_tokens=max_tokens,
                ),
            )
            return r.text
        except Exception:
            if attempt == 2:
                raise
            time.sleep(5 * (attempt + 1))

def ask_json(prompt):
    for attempt in range(3):
        try:
            r = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="Return ONLY valid JSON. No commentary.",
                    response_mime_type="application/json",
                ),
            )
            text = re.sub(r"```json|```", "", r.text).strip()
            return json.loads(text)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(5 * (attempt + 1))