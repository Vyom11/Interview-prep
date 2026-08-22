from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class Sentiment(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"


class ReviewAnalysis(BaseModel):
    review_id: int

    sentiment: Sentiment = Field(
        description="Overall sentiment classification"
    )

    key_topics: List[str] = Field(
        description="Important topics discussed in the review"
    )

    rating_estimate: int = Field(
        ge=1,
        le=5,
        description="Estimated user rating"
    )