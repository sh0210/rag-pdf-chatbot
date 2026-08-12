from pypdf import PdfReader

def extract_text_from_pdf(file):
    """
    Extracts all text from a PDF file object.
    Returns the extracted text, or an empty string if extraction fails/no text found.
    """
    try:
        reader = PdfReader(file)

        if len(reader.pages) == 0:
            return ""

        full_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

        return full_text.strip()

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""