import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text):
    """
    Generates an embedding vector for a single piece of text.
    Returns a list of floats, or None if it fails.
    """
    if not text or not text.strip():
        return None

    try:
        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )
        return result.embeddings[0].values
    except Exception as e:
        print(f"Embedding error: {e}")
        return None


def get_embeddings_for_chunks(chunks):
    """
    Generates embeddings for a list of text chunks.
    Returns a list of (chunk_text, embedding) tuples, skipping any that fail.
    """
    results = []
    for chunk in chunks:
        embedding = get_embedding(chunk)
        if embedding is not None:
            results.append((chunk, embedding))
        else:
            print(f"Skipped a chunk due to embedding failure: {chunk[:50]}...")
    return results