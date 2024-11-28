import cohere
import os
import langid
from fastapi import HTTPException

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
cohere_client = cohere.Client(cohere_api_key)

# Cache to store previously generated responses to avoid redundant API calls
responses_cache = {}

def detect_language(text: str) -> str:
    """Detect the language of the input text using langid."""
    try:
        language, _ = langid.classify(text)
        # Mapping of language codes to full language names
        language_map = {
            "es": "Español",
            "en": "English",
            "pt": "Portugues"
        }
        # Return the mapped language name, defaulting to the code if not found
        return language_map.get(language, language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting language: {str(e)}")

def generate_answer(question: str, relevant_chunk: str) -> str:
    """
    Generate a response to the user's question using the context provided.
    Uses Cohere's LLM to generate the answer.
    """
    # Check if the answer for the question is already in the cache
    if question in responses_cache:
         # Return the cached answer if it exists
        return responses_cache[question]
    else:
    # Make an API call to Cohere to generate a response if the answer is not in the cache
    # Detect the language of the question
        language = detect_language(question)
    
        # Create a prompt based on the requirements
        prompt = f"""
        Answer to the following question: {question}, based on the context provided below.
        The answer must:
        - Be concise and clear, no longer than one sentence.
        - Be written in {language}, regardless of the language of the context.
        - Include relevant emojis summarizing the content.
        - Be in third person.
        - Be based on this context: {relevant_chunk}
        - Remember, regardless of the language of the context, the answer has to be written in {language}.
        """

        try:
            # Generate the answer using Cohere's LLM
            response = cohere_client.generate(
                model='command-xlarge-nightly',  # Cohere model
                prompt=prompt,
                max_tokens=50,  # Increased token limit for more detailed answers
                temperature=0,  # Ensures deterministic responses
            )

            # Extract and clean up the response text
            answer = response.generations[0].text.strip()
            # Store the generated answer in the cache for future use
            responses_cache[question] = answer

            return answer

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")