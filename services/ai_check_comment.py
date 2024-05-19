# sentiment_analysis.py
import json
import torch
from transformers import RobertaForSequenceClassification, AutoTokenizer
import sys

def predict_sentiment(sentence):
    # Load pre-trained model and tokenizer
    model = RobertaForSequenceClassification.from_pretrained("wonrax/phobert-base-vietnamese-sentiment")
    tokenizer = AutoTokenizer.from_pretrained("wonrax/phobert-base-vietnamese-sentiment", use_fast=False)

    # Mã hóa câu văn thành dãy các token và tạo tensor input_ids
    input_ids = tokenizer.encode(sentence, return_tensors="pt")

    # Sử dụng mô hình để dự đoán cảm xúc
    with torch.no_grad():
        outputs = model(input_ids)

    # Lấy ra xác suất của các lớp cảm xúc (NEG: tiêu cực, POS: tích cực, NEU: trung tính)
    probabilities = torch.softmax(outputs.logits, dim=1).tolist()[0]

    # Lấy ra vị trí của lớp có xác suất cao nhất
    predicted_class_index = probabilities.index(max(probabilities))

    # Xác định lớp cảm xúc tương ứng
    if predicted_class_index == 0:
        predicted_class = "NEG"  # Tiêu cực
    elif predicted_class_index == 1:
        predicted_class = "POS"  # Tích cực
    else:
        predicted_class = "NEU"  # Trung tính

    # Trả về kết quả dự đoán
    return predicted_class


