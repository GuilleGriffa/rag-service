from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from doc_processing import load_document, split_document_into_chunks
from embeddings import generate_embeddings_for_chunks, store_embeddings_in_chromadb, search_most_relevant_chunk
from llm import generate_answer

# Initialize the FastAPI application
app = FastAPI()

# Helper function to handle the document processing pipeline
async def process_document(file: UploadFile):
    """
    Process the uploaded document by splitting it into chunks and generating embeddings.
    """
    try:
        # Load and read the uploaded document
        document_text = await load_document(file)

        # Split the document into chunks
        chunks = split_document_into_chunks(document_text)

        # Generate embeddings for each chunk
        embeddings = generate_embeddings_for_chunks(chunks)

        # Store embeddings in ChromaDB
        store_embeddings_in_chromadb(chunks, embeddings)

        return chunks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {e}")

@app.post("/ask")
async def ask_question(
    user_name: str = Form(...),  # User's name
    question: str = Form(...),  # User's question
    file: UploadFile = File(...),  # File uploaded by the user
):
    
    """
    Endpoint to handle user question and document upload. The document is processed, embeddings are generated,
    stored in ChromaDB, and a relevant answer is generated using a language model.
    """

    # Process the document and generate embeddings
    chunks = await process_document(file)
    
    # Search for the most relevant chunk based on the question
    relevant_chunk = search_most_relevant_chunk(question)

    # Generate the answer using Cohere's LLM
    answer = generate_answer(question, relevant_chunk)
    
    return {"answer": answer}
