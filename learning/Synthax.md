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