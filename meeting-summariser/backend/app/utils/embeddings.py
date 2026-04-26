# from sentence_transformers import SentenceTransformer

# # Load model once (important for performance)
# model = SentenceTransformer("all-MiniLM-L6-v2")

# def get_embeddings(text_chunks):
#     """
#     Convert list of text chunks into embeddings
#     """
#     embeddings = model.encode(text_chunks)
#     return embeddings


import numpy as np

def get_embeddings(texts):
    embeddings = []

    for text in texts:
        vec = np.zeros(384)

        for word in text.split():
            idx = hash(word) % 384
            vec[idx] += 1

        embeddings.append(vec)

    return np.array(embeddings).astype("float32")