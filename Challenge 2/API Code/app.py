from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer
import torch
from sklearn.preprocessing import LabelEncoder
import numpy as np

app = Flask(__name__)

# Load model and tokenizer
model_path = './Model'  # Adjust path as necessary
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Load LabelEncoder instance
le = LabelEncoder()
le.fit(["mixed", "negative", "neutral", "positive"]) 

class SimpleDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        return item

    def __len__(self):
        return len(self.encodings['input_ids'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            # Tokenize and create dataset
            encodings = tokenizer([text], truncation=True, padding=True, max_length=128, return_tensors="pt")
            dataset = SimpleDataset(encodings)

            # Predict
            trainer = Trainer(model=model)
            predictions = trainer.predict(dataset)
            predicted_labels = torch.argmax(torch.tensor(predictions.predictions), axis=1).cpu().numpy()

            # Decode the predicted labels
            try:
                predicted_class_names = le.inverse_transform(predicted_labels.reshape(-1))
                result = predicted_class_names[0]
            except Exception as e:
                print('Error during label decoding:', str(e))
                result = 'Error decoding label'

            return render_template('index.html', result=result, text=text)
        else:
            return render_template('index.html', result="No text provided", text="")
    else:
        return render_template('index.html', result=None, text="")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Tokenize and create dataset
    encodings = tokenizer([text], truncation=True, padding=True, max_length=128, return_tensors="pt")
    dataset = SimpleDataset(encodings)

    # Predict
    trainer = Trainer(model=model)
    predictions = trainer.predict(dataset)
    predicted_labels = torch.argmax(torch.tensor(predictions.predictions), axis=1).cpu().numpy()

    # Decode the predicted labels
    try:
        predicted_class_names = le.inverse_transform(predicted_labels.reshape(-1))
    except Exception as e:
        print('Error during label decoding:', str(e))
        return jsonify({'error': 'Failed to decode labels'}), 500

    return jsonify({'text': text, 'predicted_label': predicted_class_names[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
