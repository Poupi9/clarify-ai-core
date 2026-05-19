import json
import os
from google import genai
from BaseEvaluator import BaseEvaluator
from dataset_loader import load_synthetic_data

class PromptEvaluator(BaseEvaluator):
    def __init__(self, api_key, prompt_template, model_name="gemini-2.5-flash"):
        """
        Constructor for the child class.
        Calls the parent class constructor using super() and initializes the live Gemini client.
        """
        super().__init__(api_key, prompt_template, model_name)
        self.client = genai.Client(api_key=self.api_key)

    def _clean_json(self, raw_text):
        """
        Private helper method to clean markdown wrappers (```json ... ```) 
        frequently returned by LLMs.
        """
        text = raw_text.strip()
        if text.startswith("```json"):
            text = text.replace("```json", "", 1)
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        return text.strip()

    def run_nvc_transformation(self, raw_note):
        """
        Overrides the abstract method in BaseEvaluator.
        Injects data into the prompt template, transmits it to Gemini, 
        and returns a parsed Python dictionary.
        """
        final_prompt = self.prompt_template.replace("{{content_raw}}", raw_note)
        
        try:
            # Call the live Gemini model configured in the constructor
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=final_prompt
            )
            
            # Clean and parse the string payload into a proper dictionary
            cleaned_text = self._clean_json(response.text)
            return json.loads(cleaned_text)
            
        except Exception as e:
            print(f"🚨 API Execution Failure: {e}")
            return None

