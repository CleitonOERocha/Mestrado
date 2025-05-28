
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

model_name = "CleitonOERocha/deepseek-r1-distill-llama-8B-finetuned-nfe-detection"

model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
tokenizer = AutoTokenizer.from_pretrained(model_name)

clf = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    top_k=None,
    device="cuda"   # caso não tenha cuda, use "cpu"
)

print(clf("[CLS] Destinatario: XXX BATALHAO LOG [SEP] Municipio emitente: SÃO PAULO [SEP] Descricao do produto: MICROFONE LAPELA BY-M1 PRETO P2 [SEP] Qtd: 2 [SEP] Total: 649.78"))
