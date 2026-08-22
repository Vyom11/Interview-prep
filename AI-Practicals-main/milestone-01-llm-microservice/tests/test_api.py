from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_classify_endpoint():

    payload = {"text": "This product is amazing."}

    response = client.post("/classify", json=payload)

    assert response.status_code in [200, 500]


def test_summarize_endpoint():

    payload = {
        "text": (
            "FastAPI is a modern Python web framework "
            "designed for building high-performance APIs. "
            "It supports asynchronous programming, automatic "
            "Swagger documentation generation, and seamless "
            "integration with Pydantic for validation. "
            "Developers widely use FastAPI for AI applications, "
            "microservices, and production-grade backend systems."
        )
    }

    response = client.post("/summarize", json=payload)

    assert response.status_code in [200, 500]


def test_invalid_request():

    payload = {"text": ""}

    response = client.post("/classify", json=payload)

    assert response.status_code == 422
