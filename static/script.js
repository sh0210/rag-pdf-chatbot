const chatHistory = document.getElementById("chat-history");
let sourceCounter = 0;

function addUserMessage(question) {
    const row = document.createElement("div");
    row.className = "bubble-row user";

    const bubble = document.createElement("div");
    bubble.className = "bubble user";
    bubble.innerText = question;

    row.appendChild(bubble);
    chatHistory.appendChild(row);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function addBotMessage(answer, sources = [], isError = false) {
    const row = document.createElement("div");
    row.className = "bubble-row bot";

    const bubble = document.createElement("div");
    bubble.className = isError ? "bubble bot error" : "bubble bot";
    bubble.innerText = answer;
    row.appendChild(bubble);

    if (sources && sources.length > 0) {
        sourceCounter++;
        const toggleId = `sources-${sourceCounter}`;

        const toggle = document.createElement("div");
        toggle.className = "sources-toggle";
        toggle.innerText = `View ${sources.length} source excerpt(s) used`;

        const box = document.createElement("div");
        box.className = "sources-box";
        box.id = toggleId;

        sources.forEach((src, i) => {
            const item = document.createElement("div");
            item.className = "source-item";
            item.innerHTML = `<span class="source-distance">Excerpt ${i + 1} (distance: ${src.distance.toFixed(3)})</span><br>${src.text.slice(0, 200)}...`;
            box.appendChild(item);
        });

        toggle.addEventListener("click", () => {
            box.classList.toggle("open");
        });

        row.appendChild(toggle);
        row.appendChild(box);
    }

    chatHistory.appendChild(row);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function addLoadingBubble() {
    const row = document.createElement("div");
    row.className = "bubble-row bot";
    row.id = "loading-row";

    const bubble = document.createElement("div");
    bubble.className = "bubble bot loading";
    bubble.innerText = "Thinking...";

    row.appendChild(bubble);
    chatHistory.appendChild(row);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function removeLoadingBubble() {
    const row = document.getElementById("loading-row");
    if (row) row.remove();
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
    addUserMessage(question);
    addLoadingBubble();

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: question })
        });
        const data = await response.json();

        removeLoadingBubble();

        if (response.ok) {
            addBotMessage(data.answer, data.retrieved_chunks);
        } else {
            addBotMessage(`Error: ${data.error}`, [], true);
        }
    } catch (err) {
        removeLoadingBubble();
        addBotMessage("Something went wrong. Check console.", [], true);
        console.error(err);
    }
}

document.getElementById("ask-btn").addEventListener("click", askQuestion);

document.getElementById("question-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
        askQuestion();
    }
});

document.getElementById("clear-btn").addEventListener("click", async () => {
    chatHistory.innerHTML = "";
    sourceCounter = 0;
    try {
        await fetch("/clear-chat", { method: "POST" });
    } catch (err) {
        console.error("Failed to clear server-side history:", err);
    }
});
