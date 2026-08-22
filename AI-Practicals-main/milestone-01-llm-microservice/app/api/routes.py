from app.services.bedrock_service import BedrockService
from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    ClassificationRequest,
    ClassificationResponse,
    SummaryRequest,
    SummaryResponse,
)

router = APIRouter()

service = BedrockService()


@router.post("/classify", response_model=ClassificationResponse)
async def classify_text(request: ClassificationRequest) -> ClassificationResponse:

    try:
        result = service.classify_text(request.text)

        return ClassificationResponse(**result)

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/summarize", response_model=SummaryResponse)
async def summarize_text(request: SummaryRequest) -> SummaryResponse:

    try:
        result = service.summarize_text(request.text)

        return SummaryResponse(summary=result)

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
