# RAG System for Question Answering

## Project Overview

This project is a Retrieval-Augmented Generation (RAG) system that allows users to ask questions and receive relevant answers based on the content of a pre-processed document. The document is automatically processed at startup, its text is split into chunks, and embeddings are generated and stored in ChromaDB. When a user asks a question, the system retrieves the most relevant chunk and uses Cohere's large language model (LLM) to generate a concise, one-sentence answer in the same language as the question.

## Features

- **Automated Document Processing**: A specific document (in DOCX format) is automatically loaded, processed, and prepared for querying when the system starts.
- **Text Chunking**: The document is split into smaller chunks for easier processing and embedding.
- **Embedding Generation**: Text chunks are transformed into embeddings using Cohere's API.
- **ChromaDB Storage**: The embeddings and corresponding text chunks are stored in ChromaDB for efficient retrieval.
- **Question Answering**: The user can ask a question, and the system will return a relevant answer based on the most pertinent chunk of the document, generated using Cohere's LLM.

## Requirements

- Python 3.9 or higher
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

Install the required Python packages using `pip`:

```bash
   pip install -r requirements.txt
```

### 4. Set up environment variables:

Create a `.env` file in the root directory of the project, and add the following variables:

```env
COHERE_API_KEY=your_cohere_api_key
```
You can obtain a Cohere API key by signing up on the Cohere website.

## Usage 

### 1. Run the application: 

Once you have set up the environment, you can start the FastAPI application using `uvicorn`:

```bash
   uvicorn main:app --reload
```

### 2. API endpoints:

- `POST/ask`: This endpoint enables users to ask a question. The answer is derived from the most relevant chunk of the pre-processed document.

**Request Parameters:**

- user_name: (string) The name of the user.
- question: (string) The question the user wants to ask.

**Response:**

- answer: (string) The generated answer to the user's question.

Example request using `curl`:

```bash
   curl -X POST "http://127.0.0.1:8000/ask" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Guille Griffa",
    "question": "What did Emma decide to do?"
  }'

```

Example response:

```json
{
   "answer":"Emma decides to share her magical day with the town, leaving a lasting impression on everyone.🧚♀️"
   }
```

## Running with Docker

You can run the API either by building the Docker image yourself or by using a pre-built image from Docker Hub.

### 1. Build and run the Docker image locally:

To build the Docker image and run the application, follow these steps:

- Build the Docker image:

```bash
   docker build -t rag-service .
```

- Run the Docker container:

```bash
   docker run -d -p 8000:8000 rag-service
```

After running this command, the API will be accessible at `http://127.0.0.1:8000/docs`. You can also interact with the API using `curl` as described above.

### 2. Use the pre-built image from Docker Hub:

Alternatively, you can pull and run the pre-built image from Docker Hub:

- Pull the Docker image:

```bash
   docker pull guillerminagriffa/rag-api:latest
```
- Run the Docker container:

```bash
   docker run -d -p 8000:8000 guillerminagriffa/rag-api:latest
```

After running this command, the API will be accessible at `http://127.0.0.1:8000/docs`. You can also interact with the API using `curl` as described above.

### 3. Stopping the Docker container:

To stop the running Docker container, first, find the container ID using:

```bash
   docker ps
```
Then, stop the container using the container ID:

```bash
   docker stop <container_id>
```

## Directory Structure

```plaintext
.
├── main.py               # FastAPI application entry point
├── doc_processing.py     # Functions for document processing and chunking
├── embeddings.py         # Functions for generating and storing embeddings
├── llm.py                # Functions for generating answers using Cohere's LLM
├── chromadb_client.py    # Initialize and manage ChromaDB collection     
├── requirements.txt      # List of project dependencies
├── document.docx         # Document to be processed
├── Dockerfile            # Dockerfile for building the image
├── README.md             # Project documentation
```