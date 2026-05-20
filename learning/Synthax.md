## General synthax

*   **`os`** : Used to interact with your Mac's operating system. In our case, we use it to navigate file paths and check if files are actually there.
*   **`os.path.exists(file_path)`** : Used to check if the file address you provided is valid before Python attempts to open it. It prevents the program from crashing blindly.
*   **`raise FileNotFoundError(...)`** : Used to intentionally stop the script and throw a specific, readable error message when a critical file is missing (the "Fail Fast" principle).
*   **`with open(...) as file:`** : Used to safely open a file. The magic of the `with` keyword is that it automatically closes the file the moment you are done reading it, which prevents memory leaks on your computer.
*   **`json.load(file)`** : Used to read the raw text from the opened file and instantly convert it into a Python list of dictionaries.
*   **`if __name__ == "__main__":`** : Used as the most conventional way to test a program in Python. It tells Python: *"Only run the test code below if I am running this exact file directly in the terminal. If I import this function into `main.py` later, ignore the test code."*
*   **`try...except`** : Used to safely execute code that might fail. If an error occurs inside the `try` block, the program doesn't crash; instead, it jumps to the `except` block to handle the error gracefully.
*   **`len(...)`** : Used to calculate the length (total count) of items inside a list. We used it to verify we loaded exactly 50 notes.
*   **`.get('id')`** : Used to safely retrieve a specific value from a dictionary using its key. If the key 'id' doesn't exist, it simply returns `None` instead of crashing the program.
*   **`json.loads()`** : Used to turn a JSON **string** (text returned by the LLM) into a Python dictionary. Unlike `json.load()` which reads from a file, `loads` means "load **s**tring".
*   **`from module import function`** : Used to import specific tools from your own files (e.g. `from llm_client import run_nvc_prompt`) so you can reuse code across `main.py`, `evaluator.py`, etc. without rewriting it.
*   **Default parameters (`filename="results/...")`** : Used to give a function argument a fallback value. If the caller does not provide that argument, Python automatically uses the default.
*   **`.replace("old", "new")`** : Used to swap a placeholder inside a string template (e.g. replacing `{{content_raw}}` with the actual note text before sending it to the LLM).
*   **`.strip()`** : Used to remove invisible whitespace (spaces, tabs, newlines) from the start and end of a string. Essential when cleaning raw LLM output before parsing JSON.
*   **`enumerate(notes)`** : Used in a `for` loop to get both the index (`i`) and the item (`note`) at the same time. Handy for progress messages like `Note 3/50`.
*   **`if key not in data_dict:`** : Used to check whether a dictionary is **missing** a required key. Safer and more readable than trying to access a key that might not exist.
*   **`value in allowed_list`** : Used to verify that a value belongs to a strict whitelist (e.g. checking if `mood_category` is one of the five allowed emotions).
*   **`.get("key", default)`** : Same as `.get('id')`, but with a second argument: if the key is missing, Python returns your **default** (e.g. `""` for empty text) instead of `None`.
*   **Tuple unpacking (`max_ratio, min_ratio = 3.0, 0.5`)** : Used to assign multiple variables in one line. Keeps related thresholds grouped and readable.
*   **`csv.DictWriter` + `writeheader()` + `writerows()`** : Used to export a list of dictionaries to a spreadsheet-friendly CSV. Each dict key becomes a column; each dict becomes one row.
*   **`open(..., newline="", encoding="utf-8")`** : Used when writing CSV files. `newline=""` avoids extra blank lines on some systems; `encoding="utf-8"` preserves accents and emoji in your data.
*   **`sum(1 for r in results if r["status"] == "SUCCESS")`** : Used as a compact one-liner to count how many items in a list match a condition (here: how many notes succeeded).
* client.models.generate_content ?
Imagine que tu es dans un restaurant (le SDK Google) :

client : C'est le serveur qui prend ta commande.

.models : C'est le menu. Tu dis au serveur que tu veux regarder les plats (les modèles).

.generate_content : C'est l'action de commander. Tu demandes à la cuisine de "générer" ton plat.

* What it is: A bridge between your .env file and your script.

Why we use it: Python doesn't "see" the .env file by default. load_dotenv() searches your folder for a file named .env and loads the variables (like your API key) into the system's memory (os.environ).

Why os.getenv? Instead of writing API_KEY = "AIza..." in your code (which is dangerous if you share your code), you use os.getenv("KEY_NAME"). It's like calling a secret name from a vault.

*    for i in range(total_target // batch_size):
500 // 50 equals 10. It’s not a comma; it’s just division that "throws away" the decimal part.

* text = re.sub(r'[^\w\s]', '', text)This line is a "search and replace" command. Here is exactly what the code is doing, piece by piece:

re.sub(...): This stands for "Substitute." It looks for a pattern and replaces it with something else.

'': This is your replacement. Because it is completely empty, it acts as a delete button. Any pattern it finds will be erased.

r'...': The r stands for "raw string," which tells Python to read the text exactly as written without escaping characters.

[...]: The square brackets define a "group" of characters to look for.

^: Inside the brackets, the caret symbol means NOT.

\w: This represents all "word" characters (letters a-z, numbers 0-9, and underscores).

\s: This represents all "space" characters (spaces, tabs, newlines).

* X_train, X_test, y_train, y_test
* 3. DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")from_pretrained means we didn't write this 30,000-word dictionary ourselves; we downloaded Google's official dictionary.

uncased means the dictionary treats "Apple" and "apple" exactly the same to save space.
base refers to the architecture size (6 transformer layers, 768 hidden dimensions).

* texts.tolist(): Pandas DataFrames are heavy. .tolist() strips away all the heavy Pandas formatting and turns the data into a raw, lightweight Python List.

* Dataset: This is the core class you imported from the Hugging Face datasets library.

* .from_dict(): This is a "Class Method." It tells the Hugging Face Dataset class exactly how to ingest your Python dictionary and convert it into their proprietary Apache Arrow format, which stores data in memory highly efficiently.

* logits, labels = eval_pred (How can two equal one?)
The Python Mechanic: This is called Tuple Unpacking.
eval_pred is not a single number; it is a "Tuple" (a locked box) that contains exactly two arrays inside it. Python allows you to open the box and assign the first item to logits and the second item to labels in a single line of code. It is exactly the same as writing:

logits = eval_pred[0]

labels = eval_pred[1]