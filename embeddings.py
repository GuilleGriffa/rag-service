import cohere
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from chromadb_client import get_collection  

# Load environment variables
load_dotenv()

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY is not set in environment variables.")
cohere_client = cohere.Client(cohere_api_key)

# Get the collection from the centralized chromadb client
collection = get_collection()

def generate_embeddings_for_chunks(chunks: list) -> list:
    """
    Generates embeddings for each chunk of text using the Cohere API.
    :param chunks: List of text chunks to embed
    :return: List of embeddings corresponding to each chunk
    """

    try:
        embeddings = cohere_client.embed(texts=chunks).embeddings
        return embeddings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embeddings: {str(e)}")
    
def store_embeddings_in_chromadb(chunks: list, embeddings: list):
    """
    Store the text chunks and their corresponding embeddings in ChromaDB.
    :param chunks: List of text chunks
    :param embeddings: List of embeddings corresponding to each chunk
    """
    
    try:
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            document_id = f"doc_{i}"
            collection.add(
                    ids=[document_id],
                    documents=[chunk],
                    embeddings=[embedding]
                )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing embeddings in ChromaDB: {str(e)}")

def search_most_relevant_chunk(question: str) -> str:  
    """
    Search for the most relevant chunk in ChromaDB based on the question.
    :param question: The question to be used for searching the most relevant chunk
    :return: The most relevant chunk from the stored documents
    """
    try:
        question_embedding = cohere_client.embed(texts=[question]).embeddings[0]
        result = collection.query(query_embeddings=[question_embedding], n_results=1)
        if result['documents']:
            return result['documents'][0]  # Return the most relevant chunk
        else:
            raise ValueError("No relevant chunk found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching in ChromaDB: {str(e)}")





















