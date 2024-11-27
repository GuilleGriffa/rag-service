# RAG System for Question Answering

## Project Overview

This project is a Retrieval-Augmented Generation (RAG) system that allows users to upload a document, ask a question, and receive a relevant answer based on the document's content. The system processes the document, generates embeddings for text chunks, stores them in ChromaDB, and retrieves the most relevant chunk based on the user's question. Finally, it uses Cohere's large language model (LLM) to generate a concise, one-sentence answer in the same language as the question.

## Features

- **Document Upload**: Users can upload a document (in DOCX format) for processing.
- **Text Chunking**: The document is split into smaller chunks for easier processing and embedding.
- **Embedding Generation**: Text chunks are transformed into embeddings using Cohere's API.
- **ChromaDB Storage**: The embeddings and corresponding text chunks are stored in ChromaDB for efficient retrieval.
- **Question Answering**: The user can ask a question, and the system will return a relevant answer based on the most pertinent chunk of the document, generated using Cohere's LLM.

## Requirements

- Python 3.7 or higher
- Dependencies (listed in `requirements.txt`)

## Installation

To run the project locally, follow these steps:

### 1. Clone the Repository:

   ```bash
   git clone https://github.com/GuilleGriffa/rag-service.git
   cd rag-service
```

### 2. Set up a virtual environment: 

It is recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment as follows:

```bash
   conda create -n name_env
   conda activate name_env
```

### 3. Install dependencies:

Install the required Python packages using pip:

```bash
   pip install -r requirements.txt
```

### 4. Set up environment variables:

Create a .env file in the root directory of the project, and add the following variables:

```env
COHERE_API_KEY=your_cohere_api_key
```
You can obtain a Cohere API key by signing up on the Cohere website.

## Usage 

### 1. Run the application: 

Once you have set up the environment, you can start the FastAPI application using uvicorn:

```bash
   uvicorn main:app --reload
```

### 2. API endpoints:

- POSt/ask: This endpoint allows users to upload a document and ask a question. The document is processed, and an answer is generated based on the content of the most relevant chunk.

**Request Parameters:**

- user_name: (string) The name of the user.
- question: (string) The question the user wants to ask.
- file: (file) The document to be uploaded (in DOCX format).

**Response:**

- answer: (string) The generated answer to the user's question.

Example request using curl:

```bash
   curl -X 'POST' \
  'http://127.0.0.1:8000/ask' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'user_name=Guillermina' \
  -F 'question=Quien es Zara?' \
  -F 'file=@path/to/document.docx'
```

Example response:

```json
{"answer":"Zara es un valiente explorador que descubre un artefacto antiguo que podría salvar a la galaxia de una guerra intergaláctica entre los Dracorians y los Lumis. 💫🛸🌌"}
```

## Directory structure

```plaintext
.
├── main.py               # FastAPI application entry point
├── doc_processing.py     # Functions for document processing and chunking
├── embeddings.py         # Functions for generating and storing embeddings
├── llm.py                # Functions for generating answers using Cohere's LLM
├── requirements.txt      # List of project dependencies
├── .env                  # Environment variables (COHERE_API_KEY)
├── README.md             # Project documentation
```