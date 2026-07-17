# import numpy as np
# from sentence_transformers import SentenceTransformer
# from groq import Groq

# # ---------- INDEXING PHASE (done once) ----------
# documents = [
#     "To reset your password, go to Settings > Security and click 'Reset Password'.",
#     "Our office is open Monday to Friday, 9am to 6pm, and closed on public holidays.",
#     "The free plan includes 5 projects. The Pro plan includes unlimited projects.",
#     "To contact support, email help@example.com or call +1-555-0100.",
#     "You can export your data as CSV or JSON from the Account > Data page.",
# ]

# chunks = documents

# # Load embedding model
# embedder = SentenceTransformer("all-MiniLM-L6-v2")

# # Create embeddings for all chunks
# chunk_vectors = np.array(
#     embedder.encode(chunks, normalize_embeddings=True)
# )
# # ---------- HELPER FUNCTIONS ----------
# def cosine_similarity(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# def retrieve(query, k=3):
#     # Embed the query
#     qv = embedder.encode([query], normalize_embeddings=True)[0]

#     # Compute similarity scores
#     scores = [
#         cosine_similarity(qv, cv)
#         for cv in chunk_vectors
#     ]
#     # Rank chunks by similarity
#     ranked = sorted(
#         zip(scores, chunks),
#         reverse=True
#     )
#     # Return top-k chunks
#     return [(chunk, score) for score, chunk in ranked[:k]]

# # ---------- QUERY PHASE (done per question) ----------
# client = Groq()

# def answer(query, k=3):
#     # Retrieve relevant chunks
#     retrieved = retrieve(query, k=k)

#     # Build context
#     context = "\n\n".join(
#         chunk for chunk, score in retrieved
#     )

#     # Prompt for the LLM
#     prompt = f"""Answer the question using ONLY the context below.
# If the answer is not in the context, say "I don't know."

# Context:
# {context}

# Question: {query}

# Answer:"""

#     # Generate response
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         temperature=0,
#     )

#     return response.choices[0].message.content

# print(answer("Email?"))

# Above thing in Langchain

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

loader = PyPDFLoader("202351040_RESUME_Sid.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Modern LCEL chain (replaces RetrievalQA)
prompt = ChatPromptTemplate.from_template("""
Answer the question based only on the following context:

{context}

Question: {question}
""")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Run
print(chain.invoke("All project names?"))
