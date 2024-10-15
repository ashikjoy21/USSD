import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import os

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Add padding token to the tokenizer
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

# Load your custom dataset (bank messages)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dataset_path = os.path.join(project_root, 'dataset', 'dataset.txt')
print(f"Looking for dataset at: {dataset_path}")  # Add this line to check the path

# Add this check
if not os.path.exists(dataset_path):
    raise FileNotFoundError(f"The dataset file does not exist at {dataset_path}")

dataset = load_dataset('text', data_files={'train': dataset_path})

# Split dataset into training and testing sets
dataset = dataset['train'].train_test_split(test_size=0.1)

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)

tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=['text'])

# Modify dataset to include labels for training
tokenized_dataset = tokenized_dataset.map(
    lambda examples: {'labels': examples['input_ids'].copy()},
    batched=True
)

# Define training arguments
training_args = TrainingArguments(
    output_dir="../models/custom_gpt_model",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
)

# Create Trainer instance
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['test'],
    data_collator=lambda data: {
        'input_ids': torch.stack([torch.tensor(f['input_ids']) for f in data]),
        'attention_mask': torch.stack([torch.tensor(f['attention_mask']) for f in data]),
        'labels': torch.stack([torch.tensor(f['labels']) for f in data])
    }
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model and tokenizer
model.save_pretrained("../models/custom_gpt_model")
tokenizer.save_pretrained("../models/custom_gpt_model")

# Save the trainer configuration
trainer.save_model("../models/custom_gpt_model")
