import os
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

llm1 = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.5,
)

llm2 = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.5,
)

prompt = ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistant for answering questions about literature."),
    ("user","{question}")
])

chain1 = prompt | llm1 | StrOutputParser()
chain2 = prompt | llm2 | StrOutputParser()

parallel_chain = RunnableParallel(
    groq=chain1,
    gemini=chain2
)

question = "Who is the best footballer in the world?"

result = parallel_chain.invoke(
    {"question": question}
)

print("\n")

for model_name, answer in result.items():
    print(f"---{model_name.upper()} ---")
    print(answer)
    print()