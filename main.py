from fastapi import FastAPI
from doc_processing import process_and_store_document_on_start
from embeddings import  search_most_relevant_chunk
from llm import generate_answer
from pydantic import BaseModel

# Define the Pydantic model
class QuestionRequest(BaseModel):
    user_name: str
    question: str

# Initialize the FastAPI application
app = FastAPI()

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Endpoint to handle a user's question and generate a relevant answer based on a stored document.
    
    This endpoint processes the document (if not already processed), generates embeddings, 
    stores them in ChromaDB, and then uses a language model to provide an answer to the 
    user's question based on the most relevant chunk of the document.

    Parameters:
    - request (QuestionRequest): A Pydantic model containing the user's name (`user_name`) 
      and the question (`question`).
      
    Returns:
    - dict: A dictionary containing the generated answer to the user's question.

    Flow:
    1. The function checks if the document has already been processed and stored. 
    2. If not, it processes and stores the document.
    3. It then searches for the most relevant chunk of the document using the user's question.
    4. Finally, it generates and returns a concise, relevant answer based on the context of that chunk.
    """

    user_name = request.user_name
    question = request.question

    # Event to process and store the document (only once)
    await process_and_store_document_on_start()

    # Search for the most relevant chunk based on the question
    relevant_chunk = search_most_relevant_chunk(question)

    # Generate the answer using Cohere's LLM
    answer = generate_answer(question, relevant_chunk)
    
    return {"answer": answer}
