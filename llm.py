import cohere
import os
import langid
from fastapi import HTTPException

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
cohere_client = cohere.Client(cohere_api_key)

def detect_language(text: str) -> str:
    """Detect the language of the input text using langid."""
    try:
        language, _ = langid.classify(text)
        return language
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting language: {str(e)}")

def generate_answer(question: str, relevant_chunk: str) -> str:
    """
    Generate a response to the user's question using the context provided.
    Uses Cohere's LLM to generate the answer.
    """
    # Detect the language of the question
    language = detect_language(question)
   
    # Create a prompt based on the requirements
    prompt = f"""
    Respond to the following question in {language} using only one sentence, in third person, 
    with emojis summarizing the content. 
    The question is: "{question}"
    The provided context to answer is: {relevant_chunk}
    """

    try:
        # Generate the answer using Cohere's LLM
        response = cohere_client.generate(
            model='command-xlarge-nightly',  # Cohere model
            prompt=prompt,
            max_tokens=100,  # Increased token limit for more detailed answers
            temperature=0,  # Ensures deterministic responses
        )

        answer = response.generations[0].text.strip()

        return answer

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")