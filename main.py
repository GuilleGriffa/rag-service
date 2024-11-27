from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import docx
import cohere
import chromadb
import os
from dotenv import load_dotenv
from langdetect import detect

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

# Define the FastAPI app
app = FastAPI()

# Define the request model
#class QuestionRequest(BaseModel):
#    user_name: str
#    question: str

# Function to load and read a document (DOCX in this case)
def load_document(file_path):
    doc = docx.Document(file_path)
    document_text = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip() != ""])
    return document_text

# Function to split document into chunks (paragraphs in this case)
def split_document_into_chunks(document_text):
    # Split the document into chunks by paragraphs
    chunks = document_text.split("\n\n")
    return chunks

# Function to generate embeddings for chunks using Cohere
def generate_embeddings_for_chunks(chunks):
    embeddings = []
    for chunk in chunks:
        embedding = cohere_client.embed(texts=[chunk]).embeddings[0]
        embeddings.append(embedding)
    return embeddings

# Function to store embeddings in ChromaDB
def store_embeddings_in_chromadb(chunks, embeddings):
    for i, chunk in enumerate(chunks):

        document_id = f"doc_{i}"

        collection.add(
            ids=[document_id],
            documents=[chunk],  # The actual text chunk
            embeddings=[embeddings[i]]  # The corresponding embedding
        )

# Function to encode the question and search for the most relevant chunk
def search_most_relevant_chunk(question):
    question_embedding = cohere_client.embed(texts=[question]).embeddings[0]
    result = collection.query(query_embeddings=[question_embedding], n_results=1)
    return result['documents'][0]  # The chunk most relevant to the question

# def detect_language(question: str) -> str:
#     detected_lang = detect(question)
#     # Map the detected language code to the full language name
#     print(detected_lang)
#     language_map = {
#         "en": "English",
#         "es": "Spanish",
#         "fr": "French",
#         "de": "German",
#         "it": "Italian",
#         "pt": "Portuguese",
#         "ru": "Russian",
#         "zh": "Chinese",
#         "ja": "Japanese",
#         "ko": "Korean",
#         "ar": "Arabic",
#         # Add more languages if needed
#     }
#     return language_map.get(detected_lang, "English")  # Default to English if unknown

# Define a POST endpoint to handle the user's question
@app.post("/ask")
#async def ask_question(request: QuestionRequest, file: UploadFile = File(...)):
async def ask_question(
    user_name: str = Form(...),  # Accept user_name as form field
    question: str = Form(...),  # Accept question as form field
    file: UploadFile = File(...)  # Accept file as input
):
    # Print the file details to verify it's received correctly
    print(f"Received file: {file.filename}")

    # Step 1: Load and read the uploaded document
    document_text = load_document(file.filename)
    
    # Step 2: Split the document into chunks
    chunks = split_document_into_chunks(document_text)
    
    # Step 3: Generate embeddings for each chunk
    embeddings = generate_embeddings_for_chunks(chunks)
    
    # Step 4: Store the chunks and embeddings in ChromaDB
    store_embeddings_in_chromadb(chunks, embeddings)
    
    # Step 5: Search for the most relevant chunk based on the user's question
    #relevant_chunk = search_most_relevant_chunk(request.question)
    relevant_chunk = search_most_relevant_chunk(question)

    # language = detect_language(question)
    
    # Step 6: Generate the answer using the relevant chunk as context
    response = cohere_client.generate(
        model='command-xlarge-nightly',  # Cohere's LLM
        #prompt=f"Answer the following question in one sentence with emojis, in {request.user_name}'s language: {request.question}\nContext: {relevant_chunk}",
        prompt=f"Answer the following question in the same language it is asked. It is the question: {question}, in a natural and clear way in one sentence with emojis, using this context {question}\nContext: {relevant_chunk}",
        max_tokens=50,
        temperature=0.7,
    )
    
    # Extract the generated answer
    answer = response.generations[0].text.strip()
    
    return {"answer": answer}


