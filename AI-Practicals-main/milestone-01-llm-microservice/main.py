from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="LLM Microservice",
    version="1.0.0",
    description="FastAPI microservice using Amazon Bedrock"
)

app.include_router(router)
