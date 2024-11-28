from fastapi import HTTPException
import docx
from embeddings import generate_embeddings_for_chunks, store_embeddings_in_chromadb
from chromadb_client import get_collection 

# Get the collection from the chromadb client
collection = get_collection()

async def process_and_store_document_on_start():
    """
    Process the document and store it in ChromaDB if not already stored.
    """
    
    file_path = "./document.docx"  # Path to the document to process
    
    # Check if the document has already been processed
    # Check if the embeddings for this document already exist in ChromaDB
    existing_docs = collection.get()
    if len(existing_docs["ids"]) > 0:
        # Document already processed, no need to process again
        print("Document already processed and stored in ChromaDB.")
        return 
    
    try:
        # Load and read the content of a .docx file.
        doc = docx.Document(file_path)

        # Extract text from paragraphs, ignoring empty paragraphs
        document_text = "\n\n".join(para.text for para in doc.paragraphs if para.text.strip() != "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading document: {e}")
    
    # Split the document into chunks
    chunks = split_document_into_chunks(document_text)

    # Generate embeddings for each chunk
    embeddings = generate_embeddings_for_chunks(chunks)

    # Store embeddings in ChromaDB
    store_embeddings_in_chromadb(chunks, embeddings)
    
    print("Document processed and stored in ChromaDB.")
    return 

def split_document_into_chunks(document_text: str) -> list:
    """
    Split the document text into chunks (by paragraphs).
    :param document_text: Text to be split into chunks
    :return: List of text chunks
    """

    chunks = document_text.split("\n\n")
    return chunks


