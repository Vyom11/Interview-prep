from pydantic import BaseModel, Field


class ClassificationRequest(BaseModel):
    text: str = Field(min_length=3, description="Input text for classification")


class ClassificationResponse(BaseModel):
    label: str
    confidence: float


class SummaryRequest(BaseModel):
    text: str = Field(
        min_length=100, max_length=10000, description="Input text for summarization"
    )


class SummaryResponse(BaseModel):
    summary: str
