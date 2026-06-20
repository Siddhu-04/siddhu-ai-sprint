from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEmbeddings

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

#Load PDF and split into chunks
doc=PyMuPDFLoader("../Day10_RAG/202351040_RESUME_SID.pdf").load()
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
chunks = splitter.split_documents(doc)

#Generate embeddings
embedder=HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vector=embedder.embed_query("What is the candidate's name?")
#print(vector[:5])

#store in Chroma
vectorstore=Chroma.from_documents(chunks,embedder,collection_name="resume",persist_directory="./chroma_db")

#retrieve from Chroma and generate answer
llm=ChatGroq(model="llama-3.3-70b-versatile",api_key=os.getenv("GROQ_API_KEY"))
retriever=vectorstore.as_retriever(search_kwargs={"k":10})

def rag_answer(question:str)-> str:
    chunks=retriever.invoke(question)
    context="\n\n".join([c.page_content for c in chunks])
    prompt = f"""Answer the question using ONLY the context below.
If the context doesn't contain the answer, say "I don't know."
Cite the relevant excerpt.

<context>
{context}
</context>

Question: {question}
"""
    return llm.invoke(prompt).content

question="Choose the best project which could get him no rejection,state reason as well."
print(rag_answer(question))

'''
Full RAG pipeline-->
1. Load
2. Chunk
3. Embed
4. Store
5. Retrieve and Generate
'''