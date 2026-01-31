"""
FastAPI Server - REST API for Educational Content Generation

Endpoints:
- POST /generate - Generate educational content with full pipeline
- GET /health - Health check
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn

from pipeline import EducationalContentPipeline


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Educational Content Generator API",
    description="AI-powered educational content generation with automatic review and refinement",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = EducationalContentPipeline()


# ============================================================================
# Request/Response Models
# ============================================================================

class GenerateRequest(BaseModel):
    """Request body for content generation."""
    grade: int = Field(..., ge=1, le=12, description="Student grade level (1-12)")
    topic: str = Field(..., min_length=1, description="Educational topic")


class MCQResponse(BaseModel):
    question: str
    options: list[str]
    answer: str


class GeneratorOutputResponse(BaseModel):
    explanation: str
    mcqs: list[MCQResponse]


class ReviewResultResponse(BaseModel):
    status: str
    feedback: list[str]


class GenerateResponse(BaseModel):
    """Complete response from the generation pipeline."""
    grade: int
    topic: str
    initial_content: GeneratorOutputResponse
    review_result: ReviewResultResponse
    refined_content: Optional[GeneratorOutputResponse] = None
    was_refined: bool


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "name": "Educational Content Generator API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/generate", response_model=GenerateResponse)
async def generate_content(request: GenerateRequest):
    """Generate educational content for a given grade and topic."""
    try:
        result = pipeline.run(grade=request.grade, topic=request.topic)
        
        return GenerateResponse(
            grade=result.grade,
            topic=result.topic,
            initial_content=GeneratorOutputResponse(**result.initial_content),
            review_result=ReviewResultResponse(**result.review_result),
            refined_content=GeneratorOutputResponse(**result.refined_content) if result.refined_content else None,
            was_refined=result.was_refined
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
