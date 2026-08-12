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
        console.log(data);

        if (response.ok) {
    statusEl.innerText = `Embedded ${data.num_embedded}/${data.num_chunks} chunks. Vector dimension: ${data.embedding_dimension}`;
} else {
    statusEl.innerText = `Error: ${data.error}`;
}
    } catch (err) {
        statusEl.innerText = "Upload failed. Check console.";
        console.error(err);
    }
});

document.getElementById("ask-btn").addEventListener("click", () => {
    document.getElementById("answer-output").innerText = "Answering logic coming in later stages.";
});