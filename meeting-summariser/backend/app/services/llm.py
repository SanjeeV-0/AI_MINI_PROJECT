import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_answer(context, question):
    try:
        response = client.chat.completions.create(
    model="openrouter/auto",  # 🔥 THIS FIXES EVERYTHING,
            messages=[
                {
                    "role": "user",
                    "content": f"""
You are a strict assistant.

ONLY answer from the provided context.
If the answer is not present, say "Not found in the meeting".

Context:
{context}

Question:
{question}

Answer:
"""
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"