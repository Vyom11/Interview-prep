"""Run semantic similarity search using FAISS."""

# Pathlib handles cross-platform file paths.
# Pickle is used to load the original human-readable sentences.
import pickle
from pathlib import Path

# FAISS is used to perform the fast similarity search.
import faiss

# NumPy is used to format the query embedding correctly.
# SentenceTransformer is used to embed the user's search query.
from sentence_transformers import SentenceTransformer

# Define the paths for the FAISS index and the original embeddings/sentences data.
INDEX_PATH = Path("faiss_local/faiss.index")
EMBEDDINGS_PATH = Path("faiss_local/embeddings.pkl")

# Define the model. This MUST be the exact same model used to generate the original embeddings,
# otherwise the vector spaces won't match and the search will be meaningless.
MODEL_NAME = "all-MiniLM-L6-v2"


def main() -> None:
    """Perform vector similarity search."""

    # Load the SentenceTransformer model into memory.
    model = SentenceTransformer(MODEL_NAME)

    # Load the pre-built FAISS index from the disk.
    # str() is used because FAISS expects a string path, not a Path object.
    index = faiss.read_index(str(INDEX_PATH))

    # Open the pickle file to load the original text data.
    # We need this because FAISS only stores the numbers (vectors) and their IDs, not the actual text.
    with EMBEDDINGS_PATH.open("rb") as file:
        data = pickle.load(file)

    # Define the search query. This is what we want to find similar items for.
    query = "Artificial intelligence in healthcare"

    # Convert the text query into a vector embedding.
    # We pass it as a list `[query]` because the model expects a batch of inputs.
    # We also cast it to 'float32' because FAISS strictly requires 32-bit floats.
    query_embedding = model.encode([query]).astype("float32")

    # Perform the search using FAISS.
    # `k=5` means we want the top 5 most similar results.
    # Returns `distances` (similarity scores) and `indices` (the IDs of the closest vectors).
    distances, indices = index.search(query_embedding, k=5)

    # Print the query to the console for clarity.
    print(f"Query: {query}")
    print()

    # Loop through the results.
    # `indices` and `distances` are 2D arrays because you can search for multiple queries at once.
    # Since we only searched for one query, we look at the first row `[0]` of the results.
    for rank, idx in enumerate(indices[0], start=1):

        # Look up the original sentence from the pickle data using the ID (idx) returned by FAISS.
        print(f"{rank}. {data['sentences'][idx]}")

        # Print the distance score.
        # (Lower is better if using L2/Euclidean distance; Higher is better if using Inner Product/Cosine Similarity).
        print(f"Distance: {distances[0][rank - 1]}")
        print()


# Ensures that the main() function only runs if the script is executed directly.
if __name__ == "__main__":
    main()
