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

document.getElementById("ask-btn").addEventListener("click", async () => {
    const question = document.getElementById("question-input").value.trim();
    const answerEl = document.getElementById("answer-output");

    if (!question) {
        answerEl.innerText = "Please type a question.";
        return;
    }

    answerEl.innerText = "Thinking...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: question })
        });
        const data = await response.json();

        if (response.ok) {
            answerEl.innerText = data.answer;
        } else {
            answerEl.innerText = `Error: ${data.error}`;
        }
    } catch (err) {
        answerEl.innerText = "Something went wrong. Check console.";
        console.error(err);
    }
});