import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

model_path = "../model_clean"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

test_article = (
    "Climate change is one of the most pressing challenges facing humanity today. "
    "Rising global temperatures have led to more frequent and severe weather events, such as hurricanes, droughts, and floods. "
    "These changes threaten ecosystems, biodiversity, and human livelihoods around the world. "
    "Governments and organizations are working to reduce greenhouse gas emissions and promote sustainable practices. "
    "Public awareness and international cooperation are essential to addressing the environmental crisis effectively."
)

model_input = tokenizer(
    test_article,
    max_length=512,          # tutaj podajemy max_length bezpośrednio
    padding='max_length',
    truncation=True,
    return_tensors='pt'
)
model_input = {k: v.to(device) for k, v in model_input.items()}

with torch.no_grad():
    generated_ids = model.generate(
        input_ids=model_input['input_ids'],
        attention_mask=model_input['attention_mask'],
        max_length=256,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=2,
        repetition_penalty=2.0
    )

# 5. Dekodowanie
output = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

sentences = re.split(r'(?<=[.!?])\s*', output.strip())
number_of_sentences = len(sentences)

print("Wygenerowane streszczenie:\n")
print(output)
print(f"\nLiczba zdań w streszczeniu: {number_of_sentences}")
