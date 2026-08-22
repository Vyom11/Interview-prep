import json
from pathlib import Path


def save_output(data: dict, output_path: str) -> None:
    Path(output_path).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    existing_data = []

    if Path(output_path).exists():
        with open(
            output_path,
            "r",
            encoding="utf-8"
        ) as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []

    existing_data.append(data)

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(existing_data, file, indent=4)