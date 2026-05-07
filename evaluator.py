import json
from llm_client import run_nvc_prompt

def evaluate_schema(data_dict):

    """
    Checks if the dictionary contains the mandatory keys.
    Input: A Python Dictionary (NOT a string)
    """

    required_keys = ["original", "nvc", "mood_category"]
    for key in required_keys:
        if key not in data_dict:
            print(f"🚨 ERROR: {key} key is required")
            return False
    return True

def evaluate_category(data_dict):
    """
    Checks if the 'mood_category' value inside the dict matches our strict list.
    """
    allowed_categories = [
        "JOY_AFFECTION", 
        "SADNESS_PAIN", 
        "ANGER_HOSTILITY", 
        "FEAR_ANXIETY", 
        "COMPLEX_SURPRISE"
    ]

    # 1. Safely grab the value inside the locker
    # We use .get() so it doesn't crash if the key is missing
    actual_category = data_dict.get("mood_category")

    if not actual_category:
        print("CATEGORY ERROR: Key 'mood_category' is missing.")
        return False

    # 2. Compare the value (Upper-cased) to our allowed list
    if actual_category.upper() in allowed_categories:
        return True
    else:
        print(f"CATEGORY ERROR: '{actual_category}' is not an allowed category.")
        return False


def evaluate_length(data_dict):

    original = data_dict.get("original")
    nvc = data_dict.get("nvc")

    if len(original) >= 150 and (len(nvc) < len(original) * 1.5 or len(nvc) > len(original) * 0.7):
        return True
    if len(original) < 100 and (len(nvc) < len(original) * 2 or len(nvc) > len(original) * 0.5):
        return True
    return False

if __name__ == "__main__":
    sample_data = {"original": "I'm mad", "nvc": "I feel frustrated", "mood_category": "joy_affection"}
    
    if evaluate_schema(sample_data):
        print("✅ Schema test passed!")
    else:
        print("❌ Schema test failed.")
    
    if evaluate_category(sample_data):
        print("✅ mood category test passed!")
    else:
        print("❌ mood category test failed")

    if evaluate_length(sample_data):
        print("✅ length test passed!")
    else:
        print("❌ length test failed")
