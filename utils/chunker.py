def chunk_text(text, chunk_size=800, chunk_overlap=100):
    """
    Splits text into overlapping chunks.
    chunk_size: max characters per chunk
    chunk_overlap: characters repeated between consecutive chunks
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())

        start += chunk_size - chunk_overlap  # move forward, keep overlap

    return [c for c in chunks if c]