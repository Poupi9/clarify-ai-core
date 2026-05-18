import json
import os
from google import genai
from PromptEvaluator import PromptEvaluator 
from dataset_loader import load_synthetic_data
from config import GEMINI_API_KEY
from visualizer import generate_performance_chart

if __name__ == "__main__":
    print("🚀 Initializing OOP Prompt Evaluation Pipeline...")

    # 1. Configuration Setup
    API_KEY = GEMINI_API_KEY
    
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

    # 2. FIX THE INSTANTIATION: Use PromptEvaluator
    evaluator = PromptEvaluator(api_key=API_KEY, prompt_template=PROMPT_TEMPLATE)

    # 3. Load input dataset
    try:
        notes = load_synthetic_data("data/raw_data.json")
    except Exception as e:
        print(f"❌ Failed to load source file: {e}")
        notes = []

    # 4. Execute the pipeline processing loop
    for i, note in enumerate(notes):
        raw_text = note.get("content_raw", "")
        print(f"🔄 Processing Note {i+1}/{len(notes)}...")

        # Step A: Transform via the LLM method
        llm_output = evaluator.run_nvc_transformation(raw_text)

        if llm_output:
            # Step B: Grade the transformation using the inherited method
            grades = evaluator.evaluate_all(llm_output)
            
            # Step C: Consolidate data into a single tracking ledger dictionary
            result_entry = {
                "id": note.get("id"),
                "status": "SUCCESS",
                "is_schema_ok": grades["is_schema_ok"],
                "is_category_ok": grades["is_category_ok"],
                "is_length_ok": grades["is_length_ok"],
                "output": llm_output.get("nvc", "")
            }
        else:
            # Fallback error mapping for pipeline failures
            result_entry = {
                "id": note.get("id"),
                "status": "FAILED",
                "is_schema_ok": False,
                "is_category_ok": False,
                "is_length_ok": False,
                "output": "API_ERROR"
            }

        # Save the result entry directly inside the object's internal state memory list
        evaluator.results.append(result_entry)
        
        # Save progress sequentially after each entry to prevent data loss
        evaluator.export_report("results/eval_report_v1.csv")

    print("\nLaunching data visualizer...")
    try:
        generate_performance_chart("results/eval_report_v1.csv")
    except Exception as e:
        print(f"Error generating chart: {e}")

    print("\nPipeline complete! Your code is now fully Object-Oriented.")