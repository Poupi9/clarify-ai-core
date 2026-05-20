import os, json, time, csv
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Define our 2Love / NVC categories
CATEGORIES = ["JOY_AFFECTION", "SADNESS_PAIN", "ANGER_HOSTILITY", "FEAR_ANXIETY", "COMPLEX_SURPRISE"]

def generate_batch(batch_size=100):
    prompt = f"""
    Context: You are generating a synthetic dataset for an NVC (Non-Violent Communication) emotion classifier.
    The goal is to capture how real people express feelings in romantic relationships.

    Task: Generate {batch_size} unique and realistic journal entries.

    Categories to use: {", ".join(CATEGORIES)}
    Distribute them evenly: ~20 entries per category.

    Style Rules (CRITICAL — follow these exactly):
    - Write in ALL LOWERCASE. No capitalization at the start of sentences.
    - Write like someone texting or venting in a private notes app. Raw, casual, unfiltered.
    - DO NOT use the category name (e.g., "joy", "anger") inside the text itself.
    - DO NOT start entries with "I feel". Vary the sentence structures.
    - DO NOT be polite or poetic. Use contractions, slang, fragments.
    - DO NOT repeat the same scenario.

    Length distribution:
    - 40 entries must be SHORT: 1 sentence only.
    - 40 entries must be MEDIUM: 2-3 sentences.
    - 20 entries must be LONGER: 4-5 sentences.

    Gender distribution — mix across all entries:
    - Use "he/him" for ~33% of entries
    - Use "she/her" for ~33% of entries
    - Use "they/them" for ~33% of entries

    JSON Structure — output ONLY valid JSON, no markdown, no explanation:
    [
        {{
            "text": "they never take accountability for anything",
            "label": "ANGER_HOSTILITY"
        }},
        {{
            "text": "why is it always my job to fix everything",
            "label": "ANGER_HOSTILITY"
        }},
        {{
            "text": "they cancel plans with me but never with their friends. starting to see where their priorities really are.",
            "label": "SADNESS_PAIN"
        }},
        {{
            "text": "she looked so happy today and i just stood there thinking wow i really love her. like genuinely. it hit me out of nowhere.",
            "label": "JOY_AFFECTION"
        }},
        {{
            "text": "he hasn't texted back in 6 hours. i know i'm probably spiraling but i can't help it. what if something's wrong. what if it's me.",
            "label": "FEAR_ANXIETY"
        }}
    ]
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        # Clean the JSON if markdown backticks are present
        raw_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(raw_text)
    except Exception as e:
        print(f"Batch failed: {e}")
        return []

def main():
    total_target = 100
    batch_size = 100
    all_data = []

    print(f"Starting synthetic data generation (Target: {total_target})...")

    for i in range(total_target // batch_size):
        print(f"Generating batch {i+1}...")
        batch = generate_batch(batch_size)
        all_data.extend(batch)
        time.sleep(2) # Avoid rate limiting

    # Save to CSV
    output_path = "emotion_classifier/results/synthetic_emotions.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(all_data)

    print(f"Success! {len(all_data)} entries saved to {output_path}")

if __name__ == "__main__":
    main()