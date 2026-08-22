"""Generate embeddings for local FAISS indexing."""

# Pathlib provides an object-oriented way to handle file and directory paths across different operating systems.
# Pickle is used to serialize (save) and deserialize (load) Python objects to/from files.
import pickle
from pathlib import Path

# Imports the SentenceTransformer class, which lets us use pre-trained AI models to generate text embeddings.
from sentence_transformers import SentenceTransformer

# Imports a variable named SENTENCES (likely a list of strings) from a local file located at `data/sentences.py`.
from data.sentences import SENTENCES

# Define the specific pre-trained model to use. "all-MiniLM-L6-v2" is a small, fast model good for sentence similarity.
MODEL_NAME = "all-MiniLM-L6-v2"

# Define the file path where the generated embeddings will be saved.
# It points to a file named 'embeddings.pkl' inside a folder named 'faiss_local'.
OUTPUT_PATH = Path("faiss_local/embeddings.pkl")


def main() -> None:
    """Generate and store sentence embeddings."""

    # Initialize the SentenceTransformer model. This will download the model if it's not already cached locally.
    model = SentenceTransformer(MODEL_NAME)

    # Pass the list of text sentences into the model to convert them into dense vector embeddings (lists of numbers).
    embeddings = model.encode(SENTENCES)

    # Open the defined output file path in "wb" (write-binary) mode.
    with OUTPUT_PATH.open("wb") as file:

        # Use pickle to write a Python dictionary into the file.
        # This dictionary stores both the original text and the corresponding generated vectors side-by-side.
        pickle.dump(
            {
                "sentences": SENTENCES,
                "embeddings": embeddings,
            },
            file,
        )

    # Print a confirmation message to the console once the file is successfully saved.
    print(f"Saved embeddings to {OUTPUT_PATH}")


# This standard Python idiom ensures that the main() function is only executed
# if this script is run directly (e.g., `python script.py`), and NOT if it is imported into another script.
if __name__ == "__main__":
    main()
