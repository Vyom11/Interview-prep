"""Index documents and embeddings into OpenSearch."""

# Import the SentenceTransformer library, which is a popular Python framework
# for state-of-the-art text and image embeddings (built on Hugging Face transformers).
from sentence_transformers import SentenceTransformer

# Import a list of raw text strings (sentences) from a local module
from data.sentences import SENTENCES

# Import the authenticated client generator and the index name ("documents-index")
# from the previous script. This keeps our code DRY (Don't Repeat Yourself).
from opensearch_aws.create_index import INDEX_NAME, create_client

# Define the specific embedding model we want to use.
# "all-MiniLM-L6-v2" is a fast, lightweight model that maps sentences to a
# 384-dimensional dense vector space. This perfectly matches the "dimension": 384
# configuration we set up in the previous index creation script!
MODEL_NAME = "all-MiniLM-L6-v2"


def main() -> None:
    """Generate embeddings and upload documents."""

    # Initialize the ML model. The first time this runs, it will download
    # the model weights from Hugging Face to your local machine.
    model = SentenceTransformer(MODEL_NAME)

    # Initialize the secure, SigV4-authenticated OpenSearch client
    client = create_client()

    # Slice the imported list to grab only the first 50 sentences for this demo
    documents = SENTENCES[:50]

    # Pass the list of 50 text strings into the model.
    # The model processes them in a batch and outputs a numpy array/matrix of embeddings.
    # 'embeddings' is now a list of 50 vectors, where each vector contains 384 numbers.
    embeddings = model.encode(documents)

    # Use 'zip' to pair each original text string with its corresponding vector.
    # Use 'enumerate' to automatically generate a numeric index (0, 1, 2...) for the ID.
    for index, (text, embedding) in enumerate(zip(documents, embeddings)):

        # Construct the document payload exactly as defined in the previous mapping:
        # It needs a "text" field and an "embedding" field.
        document = {
            "text": text,
            # The model outputs embeddings as Numpy arrays, but OpenSearch's REST API
            # uses JSON, which does not understand Numpy arrays.
            # .tolist() converts the Numpy array into a standard Python list of floats.
            "embedding": embedding.tolist(),
        }

        # Send the document to the OpenSearch index
        client.index(
            index=INDEX_NAME,  # The target database index ("documents-index")
            body=document,  # The actual data (text + vector)
        )

    # Confirm completion in the console
    print("Indexed 50 documents")


# Standard Python idiom ensuring the code runs only when executed as a script directly
if __name__ == "__main__":
    main()
