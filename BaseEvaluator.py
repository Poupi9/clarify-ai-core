import pandas as pd

class BaseEvaluator:
    def __init__(self, api_key, prompt_template, model_name):

        self.api_key = api_key
        self.prompt_template = prompt_template
        self.model_name = model_name
        self.results = []  # This list will hold all our evaluation dictionaries

    def run_nvc_transformation(self, raw_note):
        raise NotImplementedError("This method must be overridden in a subclass.")

    def _evaluate_schema(self, data_dict):
        required_keys = ["original", "nvc", "mood_category"]
        for key in required_keys:
            if key not in data_dict:
                print(f"🚨 ERROR: {key} key is required")
                return False
        return True

    def _evaluate_category(self, data_dict):
        allowed_categories = [
            "JOY_AFFECTION", 
            "SADNESS_PAIN", 
            "ANGER_HOSTILITY", 
            "FEAR_ANXIETY", 
            "COMPLEX_SURPRISE"
        ]
        
        actual_category = data_dict.get("mood_category")
        if not actual_category:
            print("🚨 CATEGORY ERROR: Key 'mood_category' is missing.")
            return False

        if actual_category.upper() in allowed_categories:
            return True
        else:
            print(f"🚨 CATEGORY ERROR: '{actual_category}' is not an allowed category.")
            return False

    def _evaluate_length(self, data_dict):
        original_len = len(data_dict.get("original", ""))
        nvc_len = len(data_dict.get("nvc", ""))

        if original_len < 100:
            max_ratio, min_ratio = 3.0, 0.5 
        else:
            max_ratio, min_ratio = 1.8, 0.8  

        is_not_too_long = nvc_len <= (original_len * max_ratio)
        is_not_too_short = nvc_len >= (original_len * min_ratio)

        if is_not_too_long and is_not_too_short:
            return True
        else:
            print(f"🚨 LENGTH ERROR: Original({original_len}) vs NVC({nvc_len})")
            return False

    def evaluate_all(self, data_dict):
        return {
            "is_schema_ok": self._evaluate_schema(data_dict),
            "is_category_ok": self._evaluate_category(data_dict),
            "is_length_ok": self._evaluate_length(data_dict)
        }

    def export_report(self, filename="results/eval_report_v1.csv"):
        if not self.results:
            print("No data to export.")
            return
        
        # 1. Convert state memory to DataFrame
        df = pd.DataFrame(self.results)

        # 2. Save CSV
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"Report saved successfully to {filename}")

        # 3. Print Analytics
        print("\n--- AGGREGATE ANALYTICS ---")
        total_notes = len(df)
        success_api = df[df.get('status', 'SUCCESS') == 'SUCCESS'].shape[0]
        
        print(f"Total Processed: {total_notes}")
        print(f"API Success Rate: {(success_api / total_notes) * 100:.1f}%")
        print(f"Schema Passing Rate: {df['is_schema_ok'].mean() * 100:.1f}%")
        print(f"Category Passing Rate: {df['is_category_ok'].mean() * 100:.1f}%")
        print(f"Length Passing Rate: {df['is_length_ok'].mean() * 100:.1f}%")