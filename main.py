from dataset_loader import load_synthetic_data
from llm_client import run_nvc_prompt
from evaluator import evaluate_schema, evaluate_category, evaluate_length
import csv
import os
import pandas as pd

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

def save_results_to_csv(results, filename="results/eval_report_v1.csv"):
    if not results:
        return
    
    df = pd.DataFrame(results)

    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Report saved successfully to {filename}")

    # 3. Task 5.3: Print instant aggregate analytics
    print("\n--- AGGREGATE ANALYTICS ---")
    total_notes = len(df)
    success_api = df[df['status'] == 'SUCCESS'].shape[0]
    
    print(f"Total Processed: {total_notes}")
    print(f"API Success Rate: {(success_api / total_notes) * 100:.1f}%")
    print(f"Schema Passing Rate: {df['is_schema_ok'].mean() * 100:.1f}%")
    print(f"Category Passing Rate: {df['is_category_ok'].mean() * 100:.1f}%")
    print(f"Length Passing Rate: {df['is_length_ok'].mean() * 100:.1f}%")


def main():

    # 1. Load the notes
    try:
        notes = load_synthetic_data("data/raw_data.json")
    except Exception as e:
        print(f"Could not load data: {e}")
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
    print(f"Successfully processed {success_count}/{len(notes)} notes.")

    save_results_to_csv(results, "results/eval_report_v1.csv")
    
    return results

if __name__ == "__main__":
    final_results = main()
    # For now, let's just see the first result to verify
    if final_results:
        print(f"\nSample Result: {final_results[0]}")