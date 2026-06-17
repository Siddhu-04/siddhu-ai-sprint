import os,time
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from pinecone import Pinecone,ServerlessSpec
from dotenv import load_dotenv
load_dotenv()

PDF_Dir="../Day9_Vector_DB/docs/college_pdfs"
model=SentenceTransformer('all-MiniLM-L6-v2')

# Load PDF's and extract text
def load_pdfs():
    docs, names = [], []
    for file in os.listdir(PDF_Dir):
        if file.endswith('.pdf'):
            text = ''.join(page.extract_text() or '' for page in PdfReader(os.path.join(PDF_Dir, file)).pages)
            if text.strip():
                docs.append(text)
                names.append(file)
    return docs, names
docs,names=load_pdfs()
embeddings=model.encode(docs).tolist()

# Chroma
client = chromadb.PersistentClient(path="./chroma_db")
try:
    client.delete_collection("college_pdfs")
except Exception:
    pass
collection = client.create_collection(name="college_pdfs")

collection.add(ids=[str(i) for i in range(len(docs))], documents=docs, embeddings=embeddings)
t = time.perf_counter()

# Pinecone
pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "college-pdfs"
if index_name not in [i.name for i in pinecone.list_indexes()]:
    pinecone.create_index(index_name, dimension=len(embeddings[0]), metric="cosine",spec=ServerlessSpec(cloud='aws', region='us-east-1'))
index = pinecone.Index(index_name)
index.upsert(vectors=[(str(i), embeddings[i], {'text': docs[i][:300], 'file': names[i]}) for i in range(len(docs))])
t = time.perf_counter()

# Querying
QUERIES = [
    'Explain normalization',
    'How does gradient descent work?',
    'What is process scheduling?',
    'Describe Newton laws of motion',
    'What is the Fourier transform?',
]

print(f"{'Query':<40} {'Chroma':>10} {'Pinecone':>12}")
print('-' * 65)

for query in QUERIES:
    q = model.encode(query).tolist()

    t = time.perf_counter()
    r1 = collection.query(query_embeddings=[q], n_results=3)
    ch = (time.perf_counter()-t)*1000

    t = time.perf_counter()
    r2 = index.query(vector=q, top_k=3, include_metadata=True)
    pn = (time.perf_counter()-t)*1000

    print(f'\n{query}')
    print(f'  Latency -> Chroma: {ch:.1f}ms | Pinecone: {pn:.1f}ms')

    print('  Chroma answer:')
    print('   file:', names[int(r1["ids"][0][0])])
    print('   text:', r1['documents'][0][0][:200].replace('\n', ' '))

    print('  Pinecone answer:')
    print('   file:', r2['matches'][0]['metadata']['file'])
    print('   text:', r2['matches'][0]['metadata']['text'][:200].replace('\n', ' '))