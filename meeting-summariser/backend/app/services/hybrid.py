from rank_bm25 import BM25Okapi

class BM25Retriever:
    def __init__(self, documents):
        self.tokenized = [doc.split() for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized)
        self.docs = documents

    def search(self, query, k=3):
        scores = self.bm25.get_scores(query.split())
        top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [self.docs[i] for i in top_idx]