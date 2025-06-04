import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_path = "../model_sentenum"
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

max_input = 512

model_input = tokenizer(
    test_article,
    max_length=max_input,
    padding='max_length',
    truncation=True,
    return_tensors='pt'
)

forced_tokens = [tokenizer.convert_tokens_to_ids(f"[SN]{i}") for i in range(1, 11)] # dla 10 zdań
# forced_tokens = [tokenizer.convert_tokens_to_ids(f"[SN]{i}") for i in range(1, 6)] # dla 6 zdań
# forced_tokens = [tokenizer.convert_tokens_to_ids(f"[SN]{i}") for i in range(1, 4)] # dla 3 zdań
force_words_ids = [[tok_id] for tok_id in forced_tokens]

model_input = {k: v.to(device) for k, v in model_input.items()}

with torch.no_grad():
    generated_ids = model.generate(
        input_ids=model_input['input_ids'],
        attention_mask=model_input['attention_mask'],
        max_length=256,
        num_beams=4,
        force_words_ids=force_words_ids,
        early_stopping=True
    )

output = tokenizer.decode(generated_ids[0], skip_special_tokens=False)

print("Wygenerowane streszczenie:\n")
print(output)

sn_tokens = [token for token in output.split() if token.startswith('[SN]')]
print(f"\nLiczba segmentów (zadań) w streszczeniu: {len(sn_tokens)}")
