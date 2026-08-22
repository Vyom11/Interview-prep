import pandas as pd

from app.retrieval import semantic_search


QUESTIONS = [
    "What are the project objectives?",
    "What are the financial risks?",
    "What technologies are discussed?"
]


def run_evaluation() -> None:
    """Run retrieval evaluation."""

    rows = []

    for question in QUESTIONS:
        response = semantic_search(question)

        top_hit = response["hits"]["hits"][0]

        rows.append(
            {
                "question": question,
                "score": top_hit["_score"],
                "source": top_hit["_source"]["source"],
                "text": top_hit["_source"]["text"][:200]
            }
        )

    dataframe = pd.DataFrame(rows)

    dataframe.to_csv(
        "results/evaluation_results.csv",
        index=False
    )

    print(dataframe)


if __name__ == "__main__":
    run_evaluation()