from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast

# 1. Your Hugging Face username and the name of your new cloud folder
REPO_NAME = "poupi9/clarify-emotion-classifier" 
LOCAL_MODEL_PATH = "./emotion_classifier_model/final_model"

print(f"📦 Loading local model from {LOCAL_MODEL_PATH}...")
# Load your custom-trained brain
model = DistilBertForSequenceClassification.from_pretrained(LOCAL_MODEL_PATH)
# Load the standard English dictionary (since we didn't change the vocabulary)
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

print(f"☁️ Pushing to Hugging Face Hub at {REPO_NAME}...")
# This will automatically create the repository and upload the 260MB files!
model.push_to_hub(REPO_NAME)
tokenizer.push_to_hub(REPO_NAME)

print("✅ SUCCESS! Your AI is now live on the internet.")