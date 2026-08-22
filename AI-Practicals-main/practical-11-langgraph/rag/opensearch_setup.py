# ==========================================
# 1. IMPORTS SECTION
# ==========================================

# Import 'boto3', the official Amazon Web Services (AWS) SDK for Python.
# We will use this to send commands directly to AWS infrastructure.
# Import 'os' to interact with the operating system and fetch environment variables.
import os

# Import Python's built-in 'time' module.
# We will use this to pause (sleep) our script so we don't overwhelm AWS with status checks.
import time

import boto3

# Import 'load_dotenv' to securely read configuration variables from a local '.env' file.
from dotenv import load_dotenv

# ==========================================
# 2. CONFIGURATION & CLIENT SETUP
# ==========================================

# Read the '.env' file and load its contents into the system's environment variables.
load_dotenv()

# Fetch the AWS region (e.g., "us-east-1" or "eu-west-1") from the environment variables.
# This tells AWS geographically where we want our server to be built.
region = os.getenv("AWS_REGION")

# Create a boto3 client specifically for the "opensearch" service.
# A "client" provides a direct, low-level interface to the AWS OpenSearch API.
client = boto3.client("opensearch", region_name=region)


# ==========================================
# 3. OPENSEARCH DOMAIN CREATION
# ==========================================

# Define the name we want to give to our new OpenSearch cluster (server).
domain_name = "langgraph-rag-domain"

# Send the command to AWS to create the OpenSearch domain.
# Note: This command just *starts* the creation process. It takes AWS 15-30 minutes to actually build it.
response = client.create_domain(
    DomainName=domain_name,  # The name we defined above.
    EngineVersion="OpenSearch_2.11",  # Specify the exact software version of OpenSearch we want.
    # Configure the computing power of the cluster (CPU/RAM).
    ClusterConfig={
        "InstanceType": "t3.small.search",  # Use a small, cost-effective instance type.
        "InstanceCount": 1,  # Only spin up 1 node (server) for this cluster.
        "DedicatedMasterEnabled": False,  # Master nodes aren't needed for a simple 1-node setup.
        "ZoneAwarenessEnabled": False,  # Multi-zone backups aren't needed for a basic setup.
    },
    # Configure the storage drive (hard drive) attached to the cluster.
    EBSOptions={
        "EBSEnabled": True,  # Enable Elastic Block Store (EBS) disk storage.
        "VolumeType": "gp3",  # Use a general-purpose SSD (gp3) for fast performance.
        "VolumeSize": 10,  # Set the storage capacity to 10 Gigabytes.
    },
)

# Print a message to the user letting them know the build process has started.
print("Creating OpenSearch domain...")


# ==========================================
# 4. MONITORING / WAITING LOOP
# ==========================================

# Start an infinite loop. We will break out of this loop manually once the server is ready.
while True:

    # Ask AWS for the current status of our specific OpenSearch domain.
    status = client.describe_domain(DomainName=domain_name)

    # Extract the "Processing" flag from the status response.
    # This is a boolean (True/False) that tells us if AWS is still building or modifying the domain.
    processing = status["DomainStatus"]["Processing"]

    # If "processing" is False, it means AWS has finished building the domain.
    if not processing:

        # Safely extract the domain's URL (Endpoint) from the status dictionary.
        # This is the web address we will use to connect to our database in the future.
        endpoint = status["DomainStatus"]["Endpoint"]

        # Print success messages and the endpoint URL.
        print("\nDomain Ready!")
        print("Endpoint:", endpoint)

        # Exit the infinite 'while' loop since our goal is complete.
        break

    # If "processing" is still True, let the user know we are still waiting.
    print("Still provisioning...")

    # Pause the script for 60 seconds before looping back to the top to check the status again.
    # This prevents us from spamming AWS with hundreds of API requests per second.
    time.sleep(60)
