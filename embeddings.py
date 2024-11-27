import cohere
import chromadb
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
cohere_client = cohere.Client(cohere_api_key)

# Initialize ChromaDB client
client = chromadb.Client()

# Create a ChromaDB collection to store the chunks and embeddings
collection_name = "documents"
collection = client.create_collection(name=collection_name)

def generate_embeddings_for_chunks(chunks: list) -> list:

    """
    Generates embeddings for each chunk of text using the Cohere API.
    :param chunks: List of text chunks to embed
    :return: List of embeddings corresponding to each chunk
    """
    embeddings = cohere_client.embed(texts=chunks).embeddings
    return embeddings

def store_embeddings_in_chromadb(chunks: list, embeddings: list):

    """
    Store the text chunks and their corresponding embeddings in ChromaDB.
    :param chunks: List of text chunks
    :param embeddings: List of embeddings corresponding to each chunk
    """
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        document_id = f"doc_{i}"
        existing_docs = collection.get(ids=[document_id])
        if len(existing_docs["ids"]) == 0:  # Si el ID no existe, agregar
            collection.add(
                ids=[document_id],
                documents=[chunk],
                embeddings=[embedding]
            )

def search_most_relevant_chunk(question: str) -> str:
    """
    Search for the most relevant chunk in ChromaDB based on the question.
    :param question: The question to be used for searching the most relevant chunk
    :return: The most relevant chunk from the stored documents
    """
    question_embedding = cohere_client.embed(texts=[question]).embeddings[0]
    result = collection.query(query_embeddings=[question_embedding], n_results=1)
    return result['documents'][0]  # Return the most relevant chunk
