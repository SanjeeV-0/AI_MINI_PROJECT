def chunk_text(text: str, chunk_size: int = 200, overlap: int = 50):
    """
    Splits text into overlapping chunks.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks