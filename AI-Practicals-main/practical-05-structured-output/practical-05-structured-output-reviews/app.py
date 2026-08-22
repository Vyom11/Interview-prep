import json
import time

from dotenv import load_dotenv
from pydantic import ValidationError

from models.review_schema import ReviewAnalysis
from services.bedrock_client import BedrockService
from utils.file_handler import load_reviews, save_results
from utils.logger import setup_logger

load_dotenv()

logger = setup_logger()


def process_review(service: BedrockService, review_data: dict) -> dict | None:
    review_id = review_data["review_id"]
    review_text = review_data["review"]

    logger.info(f"Processing review {review_id}")

    for attempt in range(3):
        try:
            response = service.analyze_review(review_text)

            response["review_id"] = review_id

            validated_response = ReviewAnalysis(**response)

            return validated_response.model_dump()

        except (json.JSONDecodeError, ValidationError) as error:
            logger.warning(
                f"Attempt {attempt + 1} failed for review {review_id}: {error}"
            )

            time.sleep(1)

        except Exception as error:
            logger.error(f"Unexpected error for review {review_id}: {error}")
            break

    return None


def main() -> None:
    """
    Main execution function.
    """

    reviews = load_reviews("data/reviews.json")

    service = BedrockService()

    results = []

    print("\nProcessing reviews...\n")

    for review in reviews:
        processed = process_review(service, review)

        if processed:
            results.append(processed)

            print("--------------------------------")
            print(f"Review ID: {processed['review_id']}")
            print(f"Sentiment: {processed['sentiment']}")
            print(f"Topics: {', '.join(processed['key_topics'])}")
            print(f"Estimated Rating: " f"{processed['rating_estimate']}/5")

    save_results(results, "outputs/structured_reviews.json")

    logger.info(f"Successfully processed {len(results)} reviews.")

    print(f"\nProcessed {len(results)} reviews successfully.")


if __name__ == "__main__":
    main()
