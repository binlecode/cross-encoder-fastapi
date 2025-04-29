# requirements.txt
# fastapi
# uvicorn
# sentence-transformers
# torch

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import CrossEncoder
import torch
from loguru import logger

# Ensure CUDA is available or use Apple's MPS if on M1/M2/M3 Mac
if torch.cuda.is_available():
    device = "cuda"
elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"
logger.info(f"Torch picked device: {device} for CrossEncoder model")

device = "cuda"
logger.info(f"Force using device: {device} for CrossEncoder model")


# Default models for cross-encoder reranking
# https://huggingface.co/BAAI/bge-reranker-v2-m3
# - lightweight, fast inference, multilingual
# - Model size: 568M params
CROSS_ENCODER_MODEL = "BAAI/bge-reranker-v2-m3"
# CROSS_ENCODER_MODEL = "BAAI/bge-reranker-base"

# Load a pretrained cross-encoder model onto GPU
logger.info(f"Loading CrossEncoder model: {CROSS_ENCODER_MODEL}")
model = CrossEncoder(
    model_name_or_path=CROSS_ENCODER_MODEL,
    device=device,
    # enable remote model loading
    trust_remote_code=True,
)
logger.info("CrossEncoder model loaded successfully")

app = FastAPI()


class RankRequest(BaseModel):
    query: str
    passages: list[str]
    top_k: int = 5  # Number of top passages to return


class RankResult(BaseModel):
    passage: str
    score: float


class RankResponse(BaseModel):
    results: list[RankResult]


@app.post("/rank", response_model=RankResponse)
def rank(req: RankRequest):
    if not req.passages:
        raise HTTPException(status_code=400, detail="Passages list is empty")
    logger.debug(f"Ranking {len(req.passages)} passages for query: {req.query}")

    top_ranked = model.rank(
        query=req.query,
        documents=req.passages,
        top_k=req.top_k,
        return_documents=True,
    )

    return RankResponse(
        results=[RankResult(passage=tr["text"], score=tr["score"]) for tr in top_ranked]
    )


@app.get("/health")
def health():
    """Health check endpoint for GKE monitoring (readiness/liveness probes)"""
    return {"status": "healthy", "model": CROSS_ENCODER_MODEL}


# To run:
# uvicorn cross_encoder_service:app --host 0.0.0.0 --port 8000 --reload
