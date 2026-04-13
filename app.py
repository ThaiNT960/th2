"""
app.py - FastAPI server cho AI Moderation Service.

Cung cấp API để Java Servlet gọi kiểm duyệt nội dung (hate speech detection).
Sử dụng PhoBERT fine-tuned trên dữ liệu tiếng Việt.

Khởi chạy:
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from utils.predict import predict, predict_batch

# ─── Khởi tạo FastAPI ──────────────────────────────────────────────────
app = FastAPI(
    title="AI Moderation Service",
    description="API phát hiện hate speech tiếng Việt bằng PhoBERT",
    version="1.0.0",
)

# ─── CORS (cho phép Java web gọi cross-origin) ─────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response Models ──────────────────────────────────────────
class ModerationRequest(BaseModel):
    """Request body cho API kiểm duyệt đơn lẻ."""
    text: str = Field(..., min_length=1, description="Nội dung cần kiểm duyệt")


class ModerationResponse(BaseModel):
    """Response body trả về kết quả kiểm duyệt."""
    label: str
    label_id: int
    confidence: float
    probabilities: dict[str, float]
    is_toxic: bool


class BatchModerationRequest(BaseModel):
    """Request body cho API kiểm duyệt hàng loạt."""
    texts: list[str] = Field(..., min_length=1, description="Danh sách nội dung cần kiểm duyệt")


class BatchModerationResponse(BaseModel):
    """Response body trả về kết quả kiểm duyệt hàng loạt."""
    results: list[ModerationResponse]
    total: int
    toxic_count: int


# ─── Endpoints ──────────────────────────────────────────────────────────
@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "service": "AI Moderation Service",
        "status": "running",
        "model": "PhoBERT Hate Speech Detector v2",
    }


@app.get("/health")
def health_check():
    """Health check cho monitoring / load balancer."""
    return {"status": "healthy"}


@app.post("/api/moderate", response_model=ModerationResponse)
def moderate_text(request: ModerationRequest):
    """
    Kiểm duyệt một đoạn text.

    - **CLEAN** (label_id=0): Nội dung bình thường
    - **OFFENSIVE** (label_id=1): Ngôn ngữ xúc phạm
    - **HATE** (label_id=2): Phát ngôn thù ghét
    """
    try:
        result = predict(request.text)
        result["is_toxic"] = result["label"] in ("OFFENSIVE", "HATE")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/api/moderate/batch", response_model=BatchModerationResponse)
def moderate_batch(request: BatchModerationRequest):
    """
    Kiểm duyệt nhiều đoạn text cùng lúc (tối ưu hiệu năng).
    Tối đa 50 texts mỗi lần gọi.
    """
    if len(request.texts) > 50:
        raise HTTPException(
            status_code=400,
            detail="Tối đa 50 texts mỗi lần gọi batch.",
        )

    try:
        raw_results = predict_batch(request.texts)
        results = []
        toxic_count = 0

        for r in raw_results:
            is_toxic = r["label"] in ("OFFENSIVE", "HATE")
            if is_toxic:
                toxic_count += 1
            r["is_toxic"] = is_toxic
            results.append(r)

        return {
            "results": results,
            "total": len(results),
            "toxic_count": toxic_count,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")


# ─── Chạy trực tiếp bằng python app.py ─────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
