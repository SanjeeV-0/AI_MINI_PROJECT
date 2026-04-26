import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.text_chunks = []
        self.metadata = []

    def add(self, embeddings, chunks, metadata_list):
        self.index.add(np.array(embeddings).astype("float32"))
        self.text_chunks.extend(chunks)
        self.metadata.extend(metadata_list)

    def search(self, query_embedding, k=3, filter_type=None):
        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"), k
        )

        results = []

        for i in indices[0]:
            if filter_type:
                if self.metadata[i]["type"] != filter_type:
                    continue

            results.append({
                "text": self.text_chunks[i],
                "meta": self.metadata[i]
            })

        return results