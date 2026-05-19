import json
import os

def load_synthetic_data(file_path="data/raw_data.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ERROR: The file '{file_path}' does not exist.")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

##test
if __name__ == "__main__":
    try:
        notes = load_synthetic_data()
        print(f"✅ Successfully loaded {len(notes)} notes.")
        print(f"🔍 First note ID: {notes[0].get('id')} | {notes[0].get('content_raw')}")
    except Exception as e:
        print(e)
