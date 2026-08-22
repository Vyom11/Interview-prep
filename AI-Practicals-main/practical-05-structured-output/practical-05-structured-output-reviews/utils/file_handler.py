import json
from pathlib import Path


def load_reviews(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_results(results: list, output_path: str) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)