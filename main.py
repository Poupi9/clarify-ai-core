from dataset_loader import load_synthetic_data
from llm_client import run_nvc_prompt
from evaluator import evaluate_schema, evaluate_category, evaluate_length

# 1. Define the Prompt Template for the whole run
PROMPT_TEMPLATE = """
Context: You are an NVC (Non-Violent Communication) therapist.
Task: Reformulate the following raw note into a constructive NVC request.

Input: {{content_raw}}

Constraint: Respond ONLY with a JSON object.
JSON Structure:
{
    "original": "the raw note text",
    "mood_category": "One of: JOY_AFFECTION, SADNESS_PAIN, ANGER_HOSTILITY, FEAR_ANXIETY, COMPLEX_SURPRISE",
    "nvc": "your reformulation"
}
"""

def main():
    
    # 1. Load the 50 notes
    try:
        notes = load_synthetic_data("data/raw_data.json")
    except Exception as e:
        print(f"❌ Could not load data: {e}")
        return

    results = []

    # 2. The Loop (Processing each note)
    for i, note in enumerate(notes):
        raw_text = note.get("content_raw", "")
        print(f"🔄 Processing Note {i+1}/{len(notes)}...")

        # Get response from Gemini
        llm_response = run_nvc_prompt(raw_text, PROMPT_TEMPLATE)

        if llm_response:
            # Run our three evaluators
            is_schema_ok = evaluate_schema(llm_response)
            is_category_ok = evaluate_category(llm_response)
            is_length_ok = evaluate_length(llm_response)

            # Store the data and the "grades"
            result_entry = {
                "id": note.get("id"),
                "status": "SUCCESS",
                "is_schema_ok": is_schema_ok,
                "is_category_ok": is_category_ok,
                "is_length_ok": is_length_ok,
                "output": llm_response.get("nvc", "")
            }
        else:
            # Handle total API failure for this note
            result_entry = {
                "id": note.get("id"),
                "status": "FAILED",
                "is_schema_ok": False,
                "is_category_ok": False,
                "is_length_ok": False,
                "output": "API_ERROR"
            }
        
        results.append(result_entry)

    # 4. Final Summary
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    print(f"\n✅ Pipeline Finished!")
    print(f"📊 Successfully processed {success_count}/{len(notes)} notes.")
    
    return results

if __name__ == "__main__":
    final_results = main()
    # For now, let's just see the first result to verify
    if final_results:
        print(f"\n👀 Sample Result: {final_results[0]}")