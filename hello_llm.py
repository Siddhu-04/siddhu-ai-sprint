import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

QUESTION = "In one sentence, what is the meaning of life?"

# Groq Client (replaces OpenAI + Anthropic)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# Model 1
resp1 = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": QUESTION}],
)
print("\n[Groq - Llama 3.1 8B Instant]")
print(resp1.choices[0].message.content)

# Model 2
resp2 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": QUESTION}],
)
print("\n[Groq - Llama 3.3 70B Versatile]")
print(resp2.choices[0].message.content)