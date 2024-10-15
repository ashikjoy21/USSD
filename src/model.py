from transformers import GPT2LMHeadModel, GPT2Tokenizer

class CustomGPTModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.load_model()

    def load_model(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_path + "/tokenizer")
        self.model = GPT2LMHeadModel.from_pretrained(self.model_path)

    def generate_text(self, input_text, max_length=50):
        inputs = self.tokenizer.encode(input_text, return_tensors='pt')
        outputs = self.model.generate(inputs, max_length=max_length, num_return_sequences=1)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
