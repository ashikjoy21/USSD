from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load and save the pre-trained model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Save the model and tokenizer
model.save_pretrained("models/custom_gpt_model")
tokenizer.save_pretrained("models/custom_gpt_model/tokenizer")
