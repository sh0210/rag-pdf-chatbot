const chatHistory = document.getElementById("chat-history");

function addMessage(question, answer, isError = false) {
    const msgEl = document.createElement("div");
    msgEl.className = "chat-message";

    const qEl = document.createElement("div");
    qEl.className = "chat-question";
    qEl.innerText = `You: ${question}`;

    const aEl = document.createElement("div");
    aEl.className = isError ? "chat-answer chat-error" : "chat-answer";
    aEl.innerText = answer;

    msgEl.appendChild(qEl);
    msgEl.appendChild(aEl);
    chatHistory.appendChild(msgEl);

    chatHistory.scrollTop = chatHistory.scrollHeight;
}

document.getElementById("upload-btn").addEventListener("click", async () => {
    const fileInput = document.getElementById("pdf-file");
    const statusEl = document.getElementById("upload-status");

    if (fileInput.files.length === 0) {
        statusEl.innerText = "Please select a PDF first.";
        return;
    }

    const formData = new FormData();
    formData.append("pdf_file", fileInput.files[0]);

    statusEl.innerText = "Uploading...";

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });
        const data = await response.json();

        if (response.ok) {
            statusEl.innerText = `Extracted ${data.char_count} chars, split into ${data.num_chunks} chunks. Embedded ${data.num_embedded}/${data.num_chunks}.`;
        } else {
            statusEl.innerText = `Error: ${data.error}`;
        }
    } catch (err) {
        statusEl.innerText = "Upload failed. Check console.";
        console.error(err);
    }
});

async function askQuestion() {
    const input = document.getElementById("question-input");
    const question = input.value.trim();

    if (!question) {
        return;
    }

    input.value = "";

    const loadingEl = document.createElement("div");
    loadingEl.className = "chat-loading";
    loadingEl.innerText = "Thinking...";
    chatHistory.appendChild(loadingEl);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: question })
        });
        const data = await response.json();

        loadingEl.remove();

        if (response.ok) {
            addMessage(question, data.answer);
        } else {
            addMessage(question, `Error: ${data.error}`, true);
        }
    } catch (err) {
        loadingEl.remove();
        addMessage(question, "Something went wrong. Check console.", true);
        console.error(err);
    }
}

document.getElementById("ask-btn").addEventListener("click", askQuestion);

document.getElementById("question-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        askQuestion();
    }
});

document.getElementById("clear-btn").addEventListener("click", () => {
    chatHistory.innerHTML = "";
});