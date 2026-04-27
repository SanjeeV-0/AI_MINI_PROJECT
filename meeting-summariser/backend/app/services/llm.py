import os
from openai import AsyncOpenAI
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

async def generate_answer(context, question, return_usage=False, response_format=None):
    try:
        kwargs = {
            "model": "openrouter/auto",
            "messages": [
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
        }
        
        if response_format:
            kwargs["response_format"] = response_format

        response = await client.chat.completions.create(**kwargs)

        content = response.choices[0].message.content
        
        if return_usage:
            usage_data = getattr(response, "usage", None)
            if usage_data:
                prompt_t = usage_data.prompt_tokens
                comp_t = usage_data.completion_tokens
                total_t = usage_data.total_tokens
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
        logger.error(f"LLM API Call failed: {str(e)}")
        if return_usage:
            return f"Error: {str(e)}", {"total_tokens": 0, "cost": 0.0}
        return f"Error: {str(e)}"