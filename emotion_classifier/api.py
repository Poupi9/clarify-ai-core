import torch
from fastapi import FastAPI
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

MODEL_PATH = "./emotion_classifier_model/final_model"

# App & global model handles 
app = FastAPI(title="Clarify Emotion Classifier", version="1.0.0")

tokenizer: DistilBertTokenizerFast = None
model: DistilBertForSequenceClassification = None
device: torch.device = None


# Startup: load model once into RAM when the server boots
@app.on_event("startup")
def load_model():
    global tokenizer, model, device

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

    print(f"🔌 Loading model from {MODEL_PATH} onto {device}...")
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
    return {"status": "ok", "model_loaded": model is not None}
