import pandas as pd
import re

class DataPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.dataframe = None
    
    def load(self):
        self.dataframe = pd.read_csv(self.file_path)
        return self.dataframe

    def process_data(self):
        self.dataframe['text'] = self.dataframe['text'].apply(self.clean_text)
        self.encode_labels()
        return self.dataframe
    
    def clean_text(self, text):
        text = str(text).lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def encode_labels(self):
        mapping = {"JOY_AFFECTION": 0, "SADNESS_PAIN": 1, "ANGER_HOSTILITY": 2, "FEAR_ANXIETY": 3, "COMPLEX_SURPRISE": 4}
        self.dataframe['label'] = self.dataframe['label'].map(mapping)


if __name__ == "__main__":
    processor = DataPreprocessor("results/synthetic_emotions.csv")
    processor.load()
    processor.process_data()
    print(processor.dataframe.head())
    

        

    


    
