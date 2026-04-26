import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the OpenAI client (pointing to OpenRouter just like your backend)
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# A small dataset of questions to test your RAG system
TEST_QUESTIONS = [
    "What was the main focus of the marketing team?",
    "Were there any discussions about budget or costs?",
    "Who is taking ownership of the new API integration?",
    "What is the capital of France?" # Trick question to test if it hallucinates or says "Not found"
]

def evaluate_rag_response(question, answer, context):
    prompt = f"""
You are a strict, expert evaluator for a Retrieval-Augmented Generation (RAG) system.
Given the User Question, the Retrieved Context, and the AI's Answer, evaluate the answer on two metrics:

1. Faithfulness (1-5): Is the answer entirely based on the provided context? (1 = Made up / hallucinates, 5 = Strictly based on context without adding outside knowledge)
2. Relevance (1-5): Does the answer directly and concisely address the user's question? (1 = Irrelevant, 5 = Perfectly relevant)

If the Answer correctly states "Not found in the meeting" when the context lacks information, Faithfulness is 5 and Relevance is 5.

Return ONLY a valid JSON object in this exact format (no markdown blocks, no extra text):
{{
    "faithfulness": 5,
    "relevance": 5,
    "reasoning": "Brief explanation of the scores."
}}

User Question: {question}

Retrieved Context (what the Vector DB found):
{context}

AI's Generated Answer:
{answer}
"""
    try:
        response = client.chat.completions.create(
            model="openrouter/auto",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        # Clean up the response in case the LLM wrapped it in markdown
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
            
        return json.loads(content)
    except Exception as e:
        return {"error": str(e), "raw": response.choices[0].message.content if 'response' in locals() else ""}

def run_evaluation():
    print("\nStarting RAG Automated Evaluation...")
    print("="*60)
    
    total_faithfulness = 0
    total_relevance = 0
    valid_evals = 0

    for i, q in enumerate(TEST_QUESTIONS, 1):
        print(f"\n[Test {i}/{len(TEST_QUESTIONS)}] Question: '{q}'")
        
        # 1. Ask the RAG system
        try:
            res = requests.post("http://127.0.0.1:8000/query", json={"question": q})
            try:
                data = res.json()
            except ValueError:
                print(f"Backend crashed! Status: {res.status_code}, Response: {res.text[:200]}")
                continue
        except requests.exceptions.ConnectionError:
            print("Backend Error: Backend is not running! Please start uvicorn first.")
            return
            
        if "error" in data:
            print(f"Backend Error: {data['error']}")
            continue
            
        answer = data.get("answer", "")
        references = data.get("references", [])
        
        # If it routed to structured data, references won't be a list of strings in the same way
        if data.get("source") == "structured":
            context = str(answer)
        else:
            context = "\n".join(references)
        
        print(f"Answer: {answer}")
        
        # 2. Evaluate the response using LLM-as-a-judge
        eval_result = evaluate_rag_response(q, answer, context)
        
        if "error" in eval_result:
            print(f"Evaluation failed: {eval_result['error']}")
            print(f"Raw output: {eval_result.get('raw')}")
            continue
            
        f_score = eval_result.get("faithfulness", 0)
        r_score = eval_result.get("relevance", 0)
        
        print(f"Scores: Faithfulness={f_score}/5 | Relevance={r_score}/5")
        print(f"Reasoning: {eval_result.get('reasoning')}")
        
        total_faithfulness += f_score
        total_relevance += r_score
        valid_evals += 1

    if valid_evals > 0:
        print("\n" + "="*60)
        print("FINAL RAG PERFORMANCE SCORECARD")
        print(f"Average Faithfulness: {total_faithfulness / valid_evals:.1f} / 5.0 (Hallucination check)")
        print(f"Average Relevance:    {total_relevance / valid_evals:.1f} / 5.0 (Usefulness check)")
        print("="*60 + "\n")

if __name__ == "__main__":
    run_evaluation()
