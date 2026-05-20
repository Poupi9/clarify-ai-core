import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from datasets import Dataset
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from transformers import TrainingArguments, Trainer
from preprocessor import DataPreprocessor

class ModelTrainer:
    def __init__(self, X_train, X_test, y_train, y_test, tokenizer, model_name="distilbert-base-uncased"):
        # 1. Assign the data
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        
        # 2. Assign the tools
        self.tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
        self.model_name = model_name
        
        # 3. The Logic Switch: Use the GPU if available, otherwise use CPU
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        
        # 4. Load the Model (The Brain) and send it to the factory (The Device)
        self.model = DistilBertForSequenceClassification.from_pretrained(
            self.model_name, 
            num_labels=5
        ).to(self.device)

    def _create_dataset(self, texts, labels):
        data_dict = {
            "text": texts.tolist(),
            "label": labels.tolist()
        }

        # Convert the dictionary into the high-speed Hugging Face Dataset format
        hf_data_dict = Dataset.from_dict(data_dict)

        return hf_data_dict
    
    def prepare_data(self):
        print("📦 Converting Pandas data to Hugging Face format...")
        
        # Create the Train and Test datasets
        self.train_dataset = self._create_dataset(self.X_train, self.y_train)
        self.test_dataset = self._create_dataset(self.X_test, self.y_test)
        
        self.tokenized_train = self.train_dataset.map(self._tokenize_function, batched=True)
        self.tokenized_test = self.test_dataset.map(self._tokenize_function, batched=True)

    def _tokenize_function(self, batch):
        return self.tokenizer(
            batch["text"], 
            padding="max_length", # Pad short sentences with 0s so they are all the same length
            truncation=True       # Chop off words if the sentence is too long
        )
    
    def compute_metrics(self, eval_pred):
        # eval_pred contains the model's guesses (logits) and the real answers (labels)
        logits, labels = eval_pred
        
        # The model outputs probabilities for all 5 classes. 
        # np.argmax picks the bucket with the highest probability.
        predictions = np.argmax(logits, axis=-1)
        
        # Calculate the Report Card
        accuracy = accuracy_score(labels, predictions)
        # We use average="weighted" because we have more than 2 categories
        f1 = f1_score(labels, predictions, average="weighted") 
        
        return {"accuracy": accuracy, "f1_score": f1}

    def train_model(self):
        print("⚙️ Setting up Training Rules...")
        
        training_args = TrainingArguments(
            output_dir="./emotion_classifier_model", # Where to save the AI's brain
            num_train_epochs=3,              # Read the study flashcards 3 times
            per_device_train_batch_size=8,   # Look at 8 sentences at a time
            per_device_eval_batch_size=8,
            eval_strategy="epoch",           # Take a practice test after every epoch
            logging_dir=None,
        )

        print("🏋️‍♂️ Initializing the Trainer...")
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.tokenized_train,
            eval_dataset=self.tokenized_test,
            compute_metrics=self.compute_metrics
        )

        print("🔥 STARTING THE GPU TRAINING LOOP...")
        trainer.train()

        print("🎓 TAKING THE FINAL EXAM (Evaluation)...")
        results = trainer.evaluate()
        
        print("\n📊 --- FINAL REPORT CARD ---")
        print(f"Accuracy: {results['eval_accuracy'] * 100:.2f}%")
        print(f"F1-Score: {results['eval_f1_score'] * 100:.2f}%")
        print("------------------------------\n")
        
        # Save the finalized, smart brain to your Mac!
        trainer.save_model("./emotion_classifier_model/final_model")
        print("✅ Custom AI successfully saved to your hard drive!")


if __name__ == "__main__":
    # --- PHASE 2: PREPROCESSING ---
    print("\n" + "="*50)
    print("🚀 STARTING PHASE 2: DATA PREPROCESSING")
    print("="*50)
    
    # Use the preprocessor we built earlier
    preprocessor = DataPreprocessor("results/synthetic_emotions.csv")
    preprocessor.load()
    preprocessor.process_data()
    
    # Import train_test_split from scikit-learn (Make sure to add this import at the top of trainer.py!)
    from sklearn.model_selection import train_test_split
    
    print("✂️ Splitting data into Study (Train) and Exam (Test) sets...")
    # X = text, y = labels. We hold back 20% for the final exam.
    X_train, X_test, y_train, y_test = train_test_split(
        preprocessor.dataframe['text'], 
        preprocessor.dataframe['label'], 
        test_size=0.2, 
        random_state=42 # Keeps the split consistent every time you run it
    )

    # --- PHASE 3: MODEL TRAINING ---
    print("\n" + "="*50)
    print("🚀 STARTING PHASE 3: MODEL TRAINING")
    print("="*50)
    
    # 1. NEW STEP: Create the tokenizer tool first
    from transformers import DistilBertTokenizerFast
    print("📚 Downloading/Loading Tokenizer...")
    tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
    
    # 2. FIX: Pass the tokenizer as the 5th argument here!
    trainer = ModelTrainer(X_train, X_test, y_train, y_test, tokenizer)
    
    # 3. Proceed with the rest
    trainer.prepare_data()
    trainer.train_model()