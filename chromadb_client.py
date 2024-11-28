import chromadb

# Initialize ChromaDB client
client = chromadb.Client()

# Create a ChromaDB collection to store the chunks and embeddings. This will be created only once
collection_name = "documents"
collection = client.get_or_create_collection(name=collection_name)

def get_collection():
    """
    Returns the ChromaDB collection.
    """
    return collection
