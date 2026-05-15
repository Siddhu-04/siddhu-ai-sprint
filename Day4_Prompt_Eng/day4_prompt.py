import os, json, re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
MODEL = "llama-3.3-70b-versatile"

SAMPLES = [
    ("DMART\nBill Dt 12-03-2026\nGrand Total Rs 1540",
     {"merchant": "dmart", "date": "2026-03-12", "total": 1540.0}),
    ("STARBUCKS PUNE\nDate: 2026/04/13\nTOTAL INR 285.00",
     {"merchant": "starbucks", "date": "2026-04-13", "total": 285.0}),
    ("BigBazaar\n05/01/2026\nNet Payable: 875.50",
     {"merchant": "bigbazaar", "date": "2026-01-05", "total": 875.5}),
    ("AMAZON FRESH\nOrder Date: January 8, 2026\nTotal Charged: Rs 349",
     {"merchant": "amazon fresh", "date": "2026-01-08", "total": 349.0}),
    ("Zomato Order\n2026-02-20\nGrand Total INR 520",
     {"merchant": "zomato", "date": "2026-02-20", "total": 520.0}),
]

def call_llm(prompt):
    raw = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=512,
    ).choices[0].message.content
    match = re.search(r"\{.*?\}", raw, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON in: {raw}")
    return json.loads(match.group())

def score(pred, exp):
    return (
        pred["merchant"].lower() == exp["merchant"]
        and pred["date"] == exp["date"]
        and float(pred["total"]) == exp["total"]
    )

def prompt_zero(text):
    return f"Extract merchant, date (YYYY-MM-DD), total. Return ONLY JSON.\n{text}"

def prompt_few(text):
    return f"""Extract receipt fields. Return ONLY JSON.

Example:
DMART\nBill Dt 12-03-2026\nGrand Total Rs 1540
{{"merchant":"DMart","date":"2026-03-12","total":1540}}

Now extract:
{text}"""

def prompt_cot(text):
    return f"""Extract merchant, date (YYYY-MM-DD), total from this receipt.
Identify each field step by step, then end with a JSON object.

Receipt: {text}

Step 1 - Merchant:
Step 2 - Date (convert to YYYY-MM-DD):
Step 3 - Total (number only):
Final JSON:"""

def evaluate(name, prompt_fn):
    correct = sum(score(call_llm(prompt_fn(t)), e) for t, e in SAMPLES)
    return name, correct, len(SAMPLES)

results = [
    evaluate("Zero-Shot",      prompt_zero),
    evaluate("Few-Shot",       prompt_few),
    evaluate("Few-Shot + CoT", prompt_cot),
]

base = results[0][1] / results[0][2]
print(f"\n{'Strategy':<18} {'Acc':>5} {'Delta':>7}")
print("-" * 33)
for name, correct, total in results:
    acc = correct / total
    print(f"{name:<18} {acc:>4.0%}  {acc - base:>+.0%}")