# ==========================================
# 1. IMPORTS SECTION
# ==========================================

# Import 'os' to fetch environment variables from the operating system.
import os

# Import 'boto3', which is the official Amazon Web Services (AWS) SDK for Python.
# It is used to interact with AWS services and retrieve AWS security credentials.
import boto3

# Import 'load_dotenv' to securely read configuration variables from a local '.env' file.
from dotenv import load_dotenv

# Import 'OpenSearch' (the main client to talk to the database) and 'RequestsHttpConnection'
# (a connection handler needed to make OpenSearch play nicely with AWS authentication).
from opensearchpy import OpenSearch, RequestsHttpConnection

# Import 'AWS4Auth' from the requests_aws4auth library.
# AWS OpenSearch requires requests to be cryptographically signed (SigV4).
# This library automatically handles that complex security signature for us.
from requests_aws4auth import AWS4Auth

# ==========================================
# 2. CONFIGURATION & AWS AUTHENTICATION
# ==========================================

# Load variables from the '.env' file into the system environment.
load_dotenv()

# Fetch the OpenSearch endpoint URL (e.g., "search-my-domain.us-east-1.es.amazonaws.com")
# and the AWS region (e.g., "us-east-1") from the environment variables.
host = os.getenv("OPENSEARCH_HOST")
region = os.getenv("AWS_REGION")

# Use boto3 to automatically find AWS credentials on your machine.
# This checks your environment variables, AWS config files (~/.aws/credentials), or IAM roles.
credentials = boto3.Session().get_credentials()

# Set up the AWS authentication object using the credentials we just fetched.
# The "es" string stands for Elasticsearch (the underlying engine OpenSearch is built on),
# which tells AWS what kind of service we are trying to securely access.
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    region,
    "es",
    session_token=credentials.token,
)


# ==========================================
# 3. OPENSEARCH CLIENT SETUP
# ==========================================

# Create the OpenSearch client instance. This acts as our bridge to the search database.
client = OpenSearch(
    hosts=[
        {"host": host, "port": 443}
    ],  # Target our specific host on the secure HTTPS port (443)
    http_auth=awsauth,  # Use the AWS4Auth object we created above to log in
    use_ssl=True,  # Encrypt the traffic (HTTPS)
    verify_certs=True,  # Ensure the server's security certificates are valid
    connection_class=RequestsHttpConnection,  # Use the requests library to handle the HTTP traffic
)


# ==========================================
# 4. INDEX (TABLE) CREATION
# ==========================================

# Define the name of the "index" we want to use.
# In OpenSearch, an "index" is conceptually similar to a "table" in a SQL database.
index_name = "company-docs"

# Check if the "company-docs" index already exists in the OpenSearch cluster.
if not client.indices.exists(index=index_name):
    # If it does not exist, tell OpenSearch to create it.
    client.indices.create(index=index_name)


# ==========================================
# 5. DATA PREPARATION & INSERTION
# ==========================================

# Define a standard Python list of dictionaries.
# Each dictionary represents a single "document" (like a row in SQL) containing text.
documents = [
    {"text": "Company leave policy allows 20 annual leaves."},
    {"text": "Remote work is allowed for engineering teams."},
    {"text": "Employees receive yearly performance bonuses."},
    {"text": "Flexible work timings are supported."},
]

# Loop through the list of documents.
# 'enumerate' automatically gives us a counter 'i' (starting at 0) and the document 'doc'.
for i, doc in enumerate(documents):

    # Insert (index) the document into OpenSearch.
    client.index(
        index=index_name,  # Tell it which index (table) to put the data in
        body=doc,  # Pass the actual dictionary containing our text
        id=i
        + 1,  # Manually assign an ID (1, 2, 3, 4) instead of letting OpenSearch generate a random one
        refresh=True,  # Forces OpenSearch to refresh the index so the data is *immediately* available for searching
    )

# Print a success message to the console to let the user know the script finished without errors.
print("Documents indexed successfully.")
