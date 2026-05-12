# Build a streaming CLI chat (text appears word-by-word)
# Use structured outputs to extract `(name, email, intent)` from user messages
# Define a `get_weather(city)` function and let GPT call it
# Refactor your code to use LiteLLM — swap providers via env var

import os, json
import litellm
from dotenv import load_dotenv
from pydantic import BaseModel, EmailStr, ValidationError

load_dotenv()

# Provider swap via env var: set MODEL=gpt-4o or MODEL=groq/llama-3.3-70b-versatile etc.
MODEL = os.getenv("MODEL", "groq/llama-3.3-70b-versatile")


# ------------------- Build a streaming CLI chat (text appears word-by-word) -------------------
print("---=== Streaming Chat ===---")
messages = []
print("Streaming CLI Chat (type exit to quit)\n")
while True:
    user = input("You: ").strip()
    if user.lower() == "exit":
        break
    messages.append({"role": "user", "content": user})
    print("AI: ", end="", flush=True)
    stream = litellm.completion(model=MODEL, messages=messages, stream=True)
    reply = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            print(delta, end="", flush=True)
            reply += delta
    print("\n")
    messages.append({"role": "assistant", "content": reply})


# ------------------- Structured outputs: extract (name, email, intent) -------------------
class UserMessage(BaseModel):
    name: str
    email: EmailStr
    intent: str

def extract_info(message: str) -> UserMessage:
    resp = litellm.completion(
        model=MODEL,
        messages=[{
            "role": "user",
            "content": (
                f"Extract name, email, and intent from this message and respond ONLY with valid JSON "
                f"matching this schema: {{\"name\": str, \"email\": str, \"intent\": str}}.\n\nMessage: '{message}'"
            )
        }],
        max_tokens=100,
        temperature=0.0
    )
    content = resp.choices[0].message.content
    try:
        return UserMessage.model_validate_json(content)
    except (ValidationError, Exception) as e:
        print("Failed to parse structured output:", e)
        return None

print("\n=== Structured Output ===")
user_input = "Hi, I'm Alice (alice@example.com). I want to know the weather."
user_info = extract_info(user_input)
if user_info:
    print(f"Name: {user_info.name}")
    print(f"Email: {user_info.email}")
    print(f"Intent: {user_info.intent}")


# ------------------- get_weather(city) with tool calling -------------------
def get_weather(city: str) -> str:
    return f"The weather in {city} is 22°C and sunny."

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

print("\n---=== Tool Calling ===---")
messages = [{"role": "user", "content": "What's the weather in Paris?"}]
resp = litellm.completion(model=MODEL, messages=messages, tools=tools, tool_choice="auto")
msg = resp.choices[0].message

if msg.tool_calls:
    for tool_call in msg.tool_calls:
        args = json.loads(tool_call.function.arguments)
        result = get_weather(args["city"])
        print(f"Tool called: get_weather({args['city']}) → {result}")
        messages += [
            {"role": "assistant", "tool_calls": [tool_call]},
            {"role": "tool", "tool_call_id": tool_call.id, "content": result}
        ]
    final = litellm.completion(model=MODEL, messages=messages)
    print("Final response:", final.choices[0].message.content)


#
