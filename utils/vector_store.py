import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # simple brute-force L2 index
        self.chunk_metadata = []  # parallel list: chunk_metadata[i] matches vector at index i

    def add_chunks(self, embedded_chunks):
        """
        embedded_chunks: list of (chunk_text, embedding) tuples
        """
        if not embedded_chunks:
            return

        vectors = np.array([emb for _, emb in embedded_chunks]).astype("float32")
        self.index.add(vectors)

        for chunk_text, _ in embedded_chunks:
            self.chunk_metadata.append({"text": chunk_text})

    def search(self, query_embedding, top_k=3):
        """
        Returns the top_k most similar chunks to the query embedding.
        """
        if self.index.ntotal == 0:
            return []

        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1:
                continue
            results.append({
                "text": self.chunk_metadata[idx]["text"],
                "distance": float(dist)
            })
        return results