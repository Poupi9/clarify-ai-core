from google import genai
from config import GEMINI_API_KEY
import json

# 1. Initialize the new client
client = genai.Client(api_key=GEMINI_API_KEY)

def generate_text(prompt):
    # 2. Call the API using the updated SDK method
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def run_nvc_prompt(raw_note, prompt_template):
    final_prompt = prompt_template.replace("{{content_raw}}", raw_note)

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=final_prompt,
        )
        raw_text = response.text
        cleaned_text = clean_and_parse_json(raw_text)
        return cleaned_text
    except Exception as e:
        print(f"🚨 ERROR: Failed to generate NVC response: {e}")
        return None
    
def clean_and_parse_json(raw_response_text):
    raw_response_text = raw_response_text.strip()
    raw_response_text = raw_response_text.replace("```json", "").replace("```", "")

    try:
        cleaned_text = json.loads(raw_response_text)
        return cleaned_text
    except Exception as e:
        print(f"🚨 ERROR: Failed to clean and parse JSON: {e}")
        return None

if __name__ == "__main__":
    prompt_template = """
        Translate this: {{content_raw}}
        Format your response as a JSON object with two keys: 'original' and 'nvc'. 
        Respond ONLY with JSON.
        """
    raw_note = "I honestly can't stand it when he just leaves his dishes in the sink. It makes me feel like his maid. Does he even respect my time?"
    nvc_content = run_nvc_prompt(raw_note, prompt_template)
    print(nvc_content)


