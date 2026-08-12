from flask import Flask, render_template, request, jsonify
from utils.pdf_processor import extract_text_from_pdf

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

    # For now, just confirm it worked — we'll store this properly in later stages
    return jsonify({
        "message": "PDF processed successfully",
        "char_count": len(text),
        "preview": text[:300]
    })

if __name__ == "__main__":
    app.run(debug=True)