"""
predict.py - Module phân loại hate speech sử dụng PhoBERT.

Labels:
    0: CLEAN     - Bình thường, không vi phạm
    1: OFFENSIVE - Ngôn ngữ xúc phạm
    2: HATE      - Phát ngôn thù ghét (hate speech)
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ─── Cấu hình ─────────────────────────────────────────────────────────
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "model", "phobert-hate-speech-final_V2")

LABEL_MAP = {
    0: "CLEAN",
    1: "OFFENSIVE",
    2: "HATE",
}

# ─── Load model & tokenizer 1 lần duy nhất khi import ─────────────────
print(f"[predict.py] Đang load model từ: {MODEL_DIR}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()  # chuyển sang chế độ inference

# Chọn device (GPU nếu có, không thì CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

print(f"[predict.py] ✅ Model loaded thành công trên {device}")


def predict(text: str) -> dict:
    """
    Phân loại một đoạn text tiếng Việt.

    Args:
        text: Chuỗi text cần kiểm tra.

    Returns:
        dict với các key:
            - label (str):       "CLEAN" | "OFFENSIVE" | "HATE"
            - label_id (int):    0 | 1 | 2
            - confidence (float): Xác suất của label được chọn (0-1)
            - probabilities (dict): Xác suất của tất cả các label
    """
    # Tokenize
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256,
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Inference (không cần tính gradient)
    with torch.no_grad():
        outputs = model(**inputs)

    # Tính xác suất
    probs = torch.softmax(outputs.logits, dim=-1)[0]
    label_id = torch.argmax(probs).item()
    confidence = probs[label_id].item()

    return {
        "label": LABEL_MAP[label_id],
        "label_id": label_id,
        "confidence": round(confidence, 4),
        "probabilities": {
            LABEL_MAP[i]: round(probs[i].item(), 4) for i in range(len(LABEL_MAP))
        },
    }


def predict_batch(texts: list[str]) -> list[dict]:
    """
    Phân loại nhiều đoạn text cùng lúc (batch prediction).

    Args:
        texts: Danh sách các chuỗi text cần kiểm tra.

    Returns:
        Danh sách các dict kết quả (giống predict()).
    """
    inputs = tokenizer(
        texts,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256,
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=-1)
    results = []

    for i in range(len(texts)):
        p = probs[i]
        label_id = torch.argmax(p).item()
        results.append({
            "label": LABEL_MAP[label_id],
            "label_id": label_id,
            "confidence": round(p[label_id].item(), 4),
            "probabilities": {
                LABEL_MAP[j]: round(p[j].item(), 4) for j in range(len(LABEL_MAP))
            },
        })

    return results
