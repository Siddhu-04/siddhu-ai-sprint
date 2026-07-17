import os
import re
import sys
import numpy as np
from pypdf import PdfReader
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PDF_PATH = sys.argv[1] if len(sys.argv) > 1 else "202351040_RESUME_Sid.pdf"


def load_chunks(pdf_path, chunk_size=450):
    reader = PdfReader(pdf_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if len(paras) <= 2:  # PDF had no blank-line breaks; fall back to per-line
        paras = [l.strip() for l in text.split("\n") if l.strip()]

    chunks, buf = [], ""
    for p in paras:
        if len(buf) + len(p) < chunk_size:
            buf += " " + p
        else:
            if buf:
                chunks.append(buf.strip())
            buf = p
    if buf:
        chunks.append(buf.strip())
    return chunks


class HybridSearcher:
    def __init__(self, chunks):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer().fit(chunks)
        self.tfidf_matrix = self.vectorizer.transform(chunks)
        self.bm25 = BM25Okapi([re.findall(r"[a-z0-9]+", c.lower()) for c in chunks])

    def _normalize(self, scores):
        m = scores.max() or 1.0
        return scores / m

    def search(self, query, k=5, w_semantic=0.6, w_bm25=0.4):
        sem = cosine_similarity(self.vectorizer.transform([query]), self.tfidf_matrix)[0]
        bm25 = np.array(self.bm25.get_scores(re.findall(r"[a-z0-9]+", query.lower())))
        combined = w_semantic * self._normalize(sem) + w_bm25 * self._normalize(bm25)
        top_idx = np.argsort(-combined)[:k]
        return [(int(i), self.chunks[i], float(combined[i])) for i in top_idx]


def get_llm_client():
    from openai import OpenAI
    if os.environ.get("GROQ_API_KEY"):
        return OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1"), "llama-3.3-70b-versatile"
    if os.environ.get("OPENAI_API_KEY"):
        return OpenAI(api_key=os.environ["OPENAI_API_KEY"]), "gpt-4o-mini"
    return None, None


def rewrite_query(query, n_variants=5):
    client, model = get_llm_client()
    if not client:
        return [query]
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content":
            f"Rewrite this search query {n_variants} different ways, one per line, no numbering: '{query}'"}],
    )
    return resp.choices[0].message.content.strip().split("\n")


def rerank(query, candidates, top_n=5):
    if os.environ.get("COHERE_API_KEY"):
        import cohere
        co = cohere.Client(api_key=os.environ["COHERE_API_KEY"])
        texts = [c[1] for c in candidates]
        result = co.rerank(query=query, documents=texts, top_n=top_n, model="rerank-english-v3.0")
        return [candidates[r.index] for r in result.results]

    client, model = get_llm_client()
    if not client:
        return sorted(candidates, key=lambda c: c[2], reverse=True)[:top_n]

    listing = "\n".join(f"{i}: {text}" for i, (_, text, _) in enumerate(candidates))
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content":
            f"Question: {query}\n\nChunks:\n{listing}\n\n"
            f"List the chunk numbers most relevant to the question, best first, comma-separated. Numbers only."}],
    )
    order = [int(n) for n in re.findall(r"\d+", resp.choices[0].message.content)]
    ranked = [candidates[i] for i in order if i < len(candidates)]
    ranked += [c for i, c in enumerate(candidates) if i not in order]
    return ranked[:top_n]


def answer(query, searcher, top_n=5):
    variants = rewrite_query(query)
    merged = {}
    for v in variants:
        for idx, text, score in searcher.search(v, k=10):
            merged[idx] = max(merged.get(idx, 0), score)
    candidates = [(i, searcher.chunks[i], s) for i, s in merged.items()]
    return rerank(query, candidates, top_n=top_n)


def generate_answer(query, top_chunks):
    client, model = get_llm_client()
    context = "\n\n".join(text for _, text, _ in top_chunks)
    if not client:
        return context  # no LLM key set - just show the raw chunks
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content":
            f"Answer the question using only the resume excerpts below. "
            f"If the excerpts don't contain the answer, say so.\n\n"
            f"Excerpts:\n{context}\n\nQuestion: {query}"}],
    )
    return resp.choices[0].message.content.strip()


if __name__ == "__main__":
    chunks = load_chunks(PDF_PATH)
    searcher = HybridSearcher(chunks)

    while True:
        query = input("\nAsk about the resume (blank to quit): ").strip()
        if not query:
            break
        top_chunks = answer(query, searcher, top_n=6)
        print("\n" + generate_answer(query, top_chunks))