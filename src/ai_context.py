from transformers import pipeline, BertTokenizer, BertForSequenceClassification
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

def extract_message_context(message):
    inputs = tokenizer(message, return_tensors="pt")
    outputs = model(**inputs)
    predicted_label = torch.argmax(outputs.logits).item()
    labels = ['Neutral', 'Important', 'Fraud']
    return labels[predicted_label]
