from flask import Flask, render_template, request, jsonify
from utils.pdf_processor import extract_text_from_pdf
from utils.chunker import chunk_text
from utils.embeddings import get_embeddings_for_chunks

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
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

    return jsonify({
        "message": "PDF processed and embedded successfully",
        "char_count": len(text),
        "num_chunks": len(chunks),
        "num_embedded": len(embedded_chunks),
        "embedding_dimension": len(embedded_chunks[0][1])
    })

if __name__ == "__main__":
    app.run(debug=True)