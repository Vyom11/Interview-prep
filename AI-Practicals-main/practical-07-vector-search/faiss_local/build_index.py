"""Build a FAISS vector index from embeddings."""

# Pathlib handles cross-platform file and directory paths.
# Pickle is used to load (deserialize) the previously saved embeddings dictionary.
import pickle
from pathlib import Path

# Imports FAISS, a highly optimized library developed by Facebook for efficient similarity search and clustering of dense vectors.
import faiss

# NumPy is used to manipulate large, multi-dimensional arrays and matrices.
import numpy as np

# Define the path to the previously saved embeddings file.
EMBEDDINGS_PATH = Path("faiss_local/embeddings.pkl")

# Define the file path where the generated FAISS index will be saved.
INDEX_PATH = Path("faiss_local/faiss.index")


def main() -> None:
    """Create and persist a FAISS index."""

    # Open the saved embeddings file in "rb" (read-binary) mode.
    with EMBEDDINGS_PATH.open("rb") as file:
        # Load the Python dictionary back into memory.
        # `data` now contains our {"sentences": [...], "embeddings": [...]}
        data = pickle.load(file)

    # Extract the embeddings, convert them into a NumPy array, and cast them to 'float32'.
    # FAISS requires input data to be strictly formatted as 32-bit floating point numbers.
    embeddings = np.array(data["embeddings"]).astype("float32")

    # Determine the dimensionality of the embeddings.
    # embeddings.shape returns (number_of_sentences, dimension_size).
    # [1] gets the dimension size (e.g., 384), which FAISS needs to know to structure its index.
    dimension = embeddings.shape[1]

    # Initialize a specific FAISS index structure.
    # IndexFlatL2 performs a brute-force exact search based on L2 (Euclidean) distance.
    # It is perfectly accurate but scales less efficiently to millions of vectors compared to approximate indexes.
    index = faiss.IndexFlatL2(dimension)

    # Insert the formatted NumPy array of embeddings into the FAISS index.
    index.add(embeddings)

    # Save the populated FAISS index to the disk.
    # str(INDEX_PATH) is used because faiss.write_index expects a plain string, not a Path object.
    faiss.write_index(index, str(INDEX_PATH))

    # Print summary information to the console confirming the number of vectors added and the save location.
    print(f"Indexed {len(embeddings)} vectors")
    print(f"Saved FAISS index to {INDEX_PATH}")


# Ensures that the main() function only runs if the script is executed directly.
if __name__ == "__main__":
    main()
