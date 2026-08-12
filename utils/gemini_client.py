import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(question, context_chunks):
    """
    Generates an answer using Gemini, given a question and retrieved context chunks.
    context_chunks: list of chunk dicts with a "text" key (from vector_store.search)
    Returns the answer string, or an error message string if generation fails.
    """
    if not context_chunks:
        return "I couldn't find any relevant information to answer this."

    context_text = "\n\n---\n\n".join(chunk["text"] for chunk in context_chunks)

    prompt = f"""Answer the question using only the context below.

Context:
{context_text}

Question: {question}

Answer:"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2
            )
        )
        return response.text
    except Exception as e:
        print(f"Gemini generation error: {e}")
        return "Sorry, something went wrong while generating the answer."