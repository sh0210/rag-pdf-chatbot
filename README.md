# RAG PDF Chatbot

A web application that lets you upload a PDF document and ask questions about it in natural language. Answers are generated using Google's Gemini LLM, grounded strictly in the content of your document through a Retrieval-Augmented Generation (RAG) pipeline — not the model's general knowledge.

**Live demo:** https://rag-pdf-chatbot-x5fg.onrender.com/
> Note: hosted on a free-tier instance that sleeps after inactivity — the first request may take 30-60 seconds to wake up.

---

## Features

- 📄 Upload any text-based PDF document
- 💬 Ask natural-language questions about its content
- 🎯 Answers are grounded in the actual document — the model explicitly states when information isn't present rather than guessing
- 🔍 View the exact source excerpts used to generate each answer (retrieval transparency)
- 🧠 Multi-turn conversation memory — follow-up questions understand prior context
- 🖥️ Clean, simple chat interface

---

## Architecture

```
                    ── INGESTION (on upload) ──
PDF file
   │
   ▼
Extract text (pypdf)
   │
   ▼
Split into overlapping chunks (~800 chars, 100 char overlap)
   │
   ▼
Generate embeddings per chunk (Gemini embedding model)
   │
   ▼
Store vectors + text in FAISS (in-memory vector index)


                    ── QUERY (on each question) ──
User question
   │
   ▼
Embed the question (same embedding model)
   │
   ▼
FAISS similarity search → top-k closest chunks
   │
   ▼
Build prompt: system instructions + retrieved chunks + 
              recent chat history + question
   │
   ▼
Gemini generates a grounded answer
   │
   ▼
Answer + source excerpts returned to the UI
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, vanilla JavaScript |
| PDF parsing | pypdf |
| Embeddings & generation | Google Gemini API (`gemini-embedding-001`, `gemini-flash-lite-latest`) |
| Vector search | FAISS (`faiss-cpu`) |
| Deployment | Render (Gunicorn WSGI server) |
| Secrets management | python-dotenv, environment variables |

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### Local Setup

```bash
git clone https://github.com/sh0210/rag-pdf-chatbot.git
cd rag-pdf-chatbot

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```

Run the app:
```bash
python app.py
```
Visit `http://127.0.0.1:5000/`

### Environment Variables
| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Gemini API key. Required for embeddings and answer generation. Loaded from `.env` (gitignored) locally; set as an environment variable directly on the hosting platform for deployment. |

---

## How It Works

1. **Text Extraction** — `pypdf` reads the uploaded PDF and extracts raw text.
2. **Chunking** — text is split into ~800-character pieces with 100-character overlap, preserving context across chunk boundaries.
3. **Embeddings** — each chunk is converted into a vector using Gemini's embedding model, capturing semantic meaning rather than surface keywords.
4. **Vector Storage** — chunks and their vectors are stored in a FAISS index for fast similarity search.
5. **Retrieval** — a question is embedded using the same model, and FAISS returns the most semantically similar chunks.
6. **Generation** — the retrieved chunks, a strict system instruction, recent chat history, and the question are sent to Gemini, which generates a grounded answer.
7. **Grounding & Hallucination Control** — the system instruction explicitly restricts the model to the provided context and requires it to state when an answer isn't present, rather than guessing.

---

## Known Limitations

- **Single document at a time.** Uploading a new PDF replaces the current one and resets conversation history.
- **Broad/whole-document questions retrieve poorly.** Fixed-size chunking and top-k retrieval mean questions like "summarize this document" or "explain chapter 3" only surface a few fragments rather than a full section. The system performs best on specific, fact-based questions.
- **No page-number tracking.** Source excerpts are shown but not mapped to specific PDF page numbers.
- **In-memory storage.** The vector store and chat history are held in server memory, not a database — they reset on server restart and don't persist across multiple users or sessions.
- **Free-tier hosting memory constraints.** The deployed instance runs on Render's free tier (512MB RAM). Large PDFs or multiple sequential uploads within a session can exceed available memory. A production deployment would use a paid tier or an external vector database (e.g., Pinecone, Weaviate) instead of in-memory FAISS.
- **Free-tier API rate limits.** The Gemini free tier enforces a daily request quota, which heavy testing can reach.

---

## Future Improvements

- Chapter/section-aware chunking for improved performance on broad summary questions
- Page-number metadata tracked through extraction → retrieval → source display
- Persistent, database-backed storage to support multiple documents and users
- Streaming responses (incremental answer rendering)
- Automated evaluation suite with test question/answer pairs and retrieval quality metrics

---

## Author

**Sharayu Patil**
[GitHub](https://github.com/sh0210) · [LinkedIn](https://linkedin.com/in/sharayu02)

Built as a hands-on project to understand Retrieval-Augmented Generation end to end — from PDF parsing through embeddings, vector search, and LLM-grounded answer generation.
