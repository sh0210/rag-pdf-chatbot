import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_INSTRUCTION = """You are a helpful assistant that answers questions using ONLY the provided document context.

Rules:
1. Answer only using information found in the context below. Do not use outside knowledge.
2. If the answer is not present in the context, clearly say "I couldn't find this in the document" — do not guess or make up an answer.
3. Be concise and direct.
4. If you're not fully certain the context answers the question, say so rather than guessing.
"""

def generate_answer(question, context_chunks):
    """
    Generates an answer using Gemini, given a question and retrieved context chunks.
    context_chunks: list of chunk dicts with a "text" key (from vector_store.search)
    Returns the answer string, or an error message string if generation fails.
    """
    if not context_chunks:
        return "I couldn't find any relevant information to answer this."

    context_text = "\n\n".join(
        f"[Excerpt {i+1}]\n{chunk['text']}"
        for i, chunk in enumerate(context_chunks)
    )

    prompt = f"""Context from the document:
{context_text}

Question: {question}

Answer the question following the system rules."""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                system_instruction=SYSTEM_INSTRUCTION
            )
        )
        return response.text
    except Exception as e:
        print(f"Gemini generation error: {e}")
        return "Sorry, something went wrong while generating the answer."