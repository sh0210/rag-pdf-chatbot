from flask import Flask, render_template, request, jsonify
from utils.pdf_processor import extract_text_from_pdf
from utils.chunker import chunk_text
from utils.embeddings import get_embeddings_for_chunks, get_embedding
from utils.vector_store import VectorStore

app = Flask(__name__)

vector_store = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    global vector_store

    if "pdf_file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["pdf_file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    text = extract_text_from_pdf(file)

    if not text:
        return jsonify({"error": "Could not extract text (empty or invalid PDF)"}), 400

    chunks = chunk_text(text)

    if not chunks:
        return jsonify({"error": "No chunks produced from this document"}), 400

    embedded_chunks = get_embeddings_for_chunks(chunks)

    if not embedded_chunks:
        return jsonify({"error": "Embedding generation failed for all chunks"}), 500

    dimension = len(embedded_chunks[0][1])
    vector_store = VectorStore(dimension)
    vector_store.add_chunks(embedded_chunks)

    return jsonify({
        "message": "PDF processed, embedded, and stored successfully",
        "char_count": len(text),
        "num_chunks": len(chunks),
        "num_embedded": len(embedded_chunks),
        "embedding_dimension": dimension
    })


@app.route("/ask", methods=["POST"])
def ask():
    global vector_store

    if vector_store is None:
        return jsonify({"error": "Please upload a PDF first"}), 400

    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    query_embedding = get_embedding(question)

    if query_embedding is None:
        return jsonify({"error": "Failed to process your question"}), 500

    retrieved_chunks = vector_store.search(query_embedding, top_k=3)

    # For now, just return retrieved chunks — Gemini answer generation comes in Stage 8-9
    return jsonify({
        "question": question,
        "retrieved_chunks": retrieved_chunks
    })


if __name__ == "__main__":
    app.run(debug=True)