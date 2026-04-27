import re
from rank_bm25 import BM25Okapi

def tokenize(text: str):
    # Lowercase and remove punctuation for better BM25 matching
    return re.sub(r'[^\w\s]', '', text.lower()).split()

class BM25Retriever:
    def __init__(self, documents):
        self.tokenized = [tokenize(doc) for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized)
        self.docs = documents

    def search(self, query, k=3):
        scores = self.bm25.get_scores(tokenize(query))
        top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [self.docs[i] for i in top_idx]