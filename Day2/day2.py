import asyncio, time, functools, random, os
from groq import AsyncGroq
from pydantic import BaseModel, EmailStr, ValidationError
from dotenv import load_dotenv

load_dotenv()


# ── 1. @retry decorator ────────────────────────────────────
def retry(attempts=3, base_delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == attempts - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    print(f"  Retry {attempt + 1} — waiting {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(attempts=3, base_delay=1.0)
def flaky_api_call(prompt: str) -> str:
    if random.random() < 0.5:
        raise ConnectionError("Simulated API timeout")
    return f"Response to: {prompt}"

# ── 2. Async parallel Groq calls ──────────────────────────
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

async def call_groq(model: str, prompt: str) -> str:
    r = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
    )
    return r.choices[0].message.content

async def parallel_llm(prompt: str):
    # Sequential — one after the other
    t0 = time.perf_counter()
    r1 = await call_groq("llama-3.3-70b-versatile", prompt)
    r2 = await call_groq("llama-3.1-8b-instant", prompt)
    seq_time = time.perf_counter() - t0
    print(f"Sequential: {seq_time:.2f}s")

    # Parallel — both at the same time
    t0 = time.perf_counter()
    r1, r2 = await asyncio.gather(
        call_groq("llama-3.3-70b-versatile", prompt),
        call_groq("llama-3.1-8b-instant", prompt),
    )
    par_time = time.perf_counter() - t0
    print(f"Parallel:   {par_time:.2f}s")
    print(f"Speedup:    {seq_time / par_time:.1f}x ⚡")
    return r1, r2

# ── 3. Pydantic model ──────────────────────────────────────
class Person(BaseModel):
    name: str
    age: int
    email: EmailStr

# ── 4. main ────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n── @retry demo ──")
    for _ in range(3):
        try:
            print(flaky_api_call("hello"))
            break
        except ConnectionError as e:
            print(f"Failed after 3 attempts: {e}")

    print("\n── Parallel LLM demo ──")
    asyncio.run(parallel_llm("What is asyncio in one sentence?"))

    print("\n── Pydantic demo ──")
    p = Person(name="Ada Lovelace", age=36, email="ada@babbage.io")
    print("Valid:", p.model_dump())
    try:
        Person(name="Bob", age="old", email="not-an-email")
    except ValidationError as e:
        print(f"Invalid: {e.error_count()} validation errors caught...")
