import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# Label mapping (mirrors preprocessor.py encode_labels) 
ID_TO_LABEL = {
    0: "JOY_AFFECTION",
    1: "SADNESS_PAIN",
    2: "ANGER_HOSTILITY",
    3: "FEAR_ANXIETY",
    4: "COMPLEX_SURPRISE",
}

MODEL_PATH = "poupi9/clarify-emotion-classifier"

# App & global model handles 
app = FastAPI(title="Clarify Emotion Classifier", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # The VIP List. "*" means "Let absolutely every website in."
    allow_credentials=True,
    allow_methods=["*"], # Allows POST, GET, OPTIONS, etc.
    allow_headers=["*"], # Allows all data headers
)

tokenizer: DistilBertTokenizerFast = None
model: DistilBertForSequenceClassification = None
device: torch.device = None


# Startup: load model once into RAM when the server boots
def load_model_if_needed():
    global tokenizer, model, device
    
    # If the model is already loaded, skip this step!
    if model is not None:
        return

    print("⏳ First request received! Loading model into RAM now...")
    # Render servers don't have Apple chips, so we force it to use the CPU
    device = torch.device("cpu") 

    print(f"🔌 Downloading model from {MODEL_PATH}...")
    tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH).to(device)
    model.eval()
    print("✅ Model ready.")


# Schemas 
class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    text: str
    emotion: str
    confidence: float


# Endpoint
@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    # 1. Check if the model is awake yet
    load_model_if_needed()

    # 2. Proceed with the normal prediction...
    inputs = tokenizer(
        request.text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=128,
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        logits = model(**inputs).logits

    probabilities = torch.softmax(logits, dim=-1)[0]
    predicted_id = int(torch.argmax(probabilities).item())
    confidence = float(probabilities[predicted_id].item())

    return PredictResponse(
        text=request.text,
        emotion=ID_TO_LABEL[predicted_id],
        confidence=round(confidence, 4),
    )


@app.get("/health")
def health():
    # 1. Check if the model is awake yet
    load_model_if_needed()

    # 2. Return the health status
    return {"status": "ok", "model_loaded": model is not None}
