import json
import os

Goal: Read the text from your JSON file and convert it into a structured Python format (List of Dictionaries) so our code can manipulate it.
Assumption: You named your file raw_data.json instead of synthetic_notes.json. The code below reflects this.
Limitation: The file must contain valid JSON. If Claude added any markdown text (like ```json) inside the file itself, the script will crash.

- Import Python's built-in json module.
- Import Python's built-in os module. (We will use this to verify the file exists).
- Define a function named load_synthetic_data.
- Give this function a single parameter named file_path.
- Set a default value for file_path pointing to your JSON file: "data/raw_data.json".

def
