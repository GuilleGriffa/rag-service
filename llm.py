import cohere
import os
import langid

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
cohere_client = cohere.Client(cohere_api_key)

def detect_language(text: str) -> str:
    """Detect the language of the input text using langid."""
    language, _ = langid.classify(text)
    return language

def generate_answer(question: str, relevant_chunk: str) -> str:
    """
    Generate a response to the user's question using the context provided.
    Uses Cohere's LLM to generate the answer.
    """
    language = detect_language(question)
    prompt=f"Answer the following question in {language}. Provide a clear and concise one-sentence answer with emojis, based on the following context: {relevant_chunk}"

    # Generate the answer
    response = cohere_client.generate(
        model='command-xlarge-nightly',  # Cohere model
        prompt=prompt,
        max_tokens=50,
        temperature=0.7,
    )
    
    answer = response.generations[0].text.strip()
    
    # Return the generated answer
    return answer