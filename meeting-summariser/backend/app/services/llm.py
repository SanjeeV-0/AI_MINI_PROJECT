import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_answer(context, question, return_usage=False):
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

        content = response.choices[0].message.content
        
        if return_usage:
            usage_data = getattr(response, "usage", None)
            if usage_data:
                prompt_t = usage_data.prompt_tokens
                comp_t = usage_data.completion_tokens
                total_t = usage_data.total_tokens
                # Assuming approximate OpenAI prices for general models:
                cost = (prompt_t / 1000) * 0.00015 + (comp_t / 1000) * 0.0006
                usage_dict = {
                    "prompt_tokens": prompt_t,
                    "completion_tokens": comp_t,
                    "total_tokens": total_t,
                    "cost": round(cost, 5)
                }
            else:
                usage_dict = {"total_tokens": 0, "cost": 0.0}
            return content, usage_dict
            
        return content

    except Exception as e:
        if return_usage:
            return f"Error: {str(e)}", {"total_tokens": 0, "cost": 0.0}
        return f"Error: {str(e)}"