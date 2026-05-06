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
