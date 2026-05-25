import base64
import os
import torch
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from pydantic import BaseModel
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

load_dotenv()

_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
    text: str = ""
    image: str | None = None  # base64-encoded image (data URL or raw)


EMOTION_CONTEXT = {
    "ANGER_HOSTILITY":  "anger, aggression, or passive hostility",
    "SADNESS_PAIN":     "sadness, emotional pain, or masked hurt",
    "FEAR_ANXIETY":     "fear, anxiety, or insecurity",
    "COMPLEX_SURPRISE": "complex feelings — confusion, being caught off guard, or mixed emotions",
    "JOY_AFFECTION":    "genuine joy or affection",
}


def gemini_translation(text: str, emotion: str) -> str:
    context = EMOTION_CONTEXT.get(emotion, emotion)
    prompt = (
        f'A person sent this message: "{text}"\n'
        f"The underlying emotion detected is: {context}.\n"
        "In exactly 1-2 sentences, explain what they really meant — be direct, "
        "insightful, and a little brutally honest. Focus on the subtext and hidden "
        "feeling, not the surface words. Do not start with 'They' every time."
    )
    try:
        response = _gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Gemini error: {e}")
        return "Translation unavailable right now."


def extract_text_from_image(image_data_url: str) -> str:
    # Strip the data URL prefix if present (e.g. "data:image/png;base64,...")
    if "," in image_data_url:
        header, b64 = image_data_url.split(",", 1)
        mime_type = header.split(":")[1].split(";")[0]
    else:
        b64 = image_data_url
        mime_type = "image/jpeg"

    image_bytes = base64.b64decode(b64)

    prompt = (
        "This is a screenshot of a private text message conversation. "
        "Extract all visible messages exactly as written. "
        "Label each line with 'Them:' or 'Me:' based on the bubble position "
        "(right-aligned = Me, left-aligned = Them). "
        "If you cannot determine the sender, just output the message text. "
        "Output only the conversation — no commentary, no explanations."
    )

    try:
        response = _gemini.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                types.Part.from_text(text=prompt),
            ],
        )
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Gemini vision error: {e}")
        return ""


class PredictResponse(BaseModel):
    text: str
    emotion: str
    confidence: float
    translation: str


# Endpoint
@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    load_model_if_needed()

    # If a screenshot is provided, extract its text via Gemini vision
    if request.image:
        extracted = extract_text_from_image(request.image)
        text = extracted if extracted else request.text
    else:
        text = request.text

    if not text:
        return PredictResponse(
            text="", emotion="COMPLEX_SURPRISE", confidence=0.0,
            translation="No text could be extracted from the image."
        )

    inputs = tokenizer(
        text,
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

    emotion = ID_TO_LABEL[predicted_id]
    translation = gemini_translation(text, emotion)

    return PredictResponse(
        text=text,
        emotion=emotion,
        confidence=round(confidence, 4),
        translation=translation,
    )


# The Front Door
@app.get("/")
def root():
    return {"message": "Clarify AI Server is awake and listening!"}

# The Side Door (Health Check)
@app.get("/health")
def health():
    # DO NOT load the model here! This must reply instantly.
    return {"status": "ok", "model_loaded": model is not None}