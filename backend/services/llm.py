import os
import json
import requests
from backend.schemas import QuizBase

def generate_quiz(text: str, url: str) -> dict:
    
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
         raise Exception("NVIDIA_API_KEY not found in environment variables. Please add it to your .env file.")

    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    
    # Construct the prompt
    prompt = f"""
    You are an expert quiz generator and knowledge extractor.
    Your task is to create a high-quality quiz ONLY from the provided Wikipedia article text.

    STRICT RULES:
    - Use only the provided article content
    - Do NOT use outside knowledge
    - Do NOT hallucinate facts not present in the text
    - Output MUST be valid JSON only
    - No markdown formatting in the output (just raw JSON)

    ARTICLE URL:
    {url}

    ARTICLE TEXT:
    {text}

    REQUIREMENTS:

    1) Generate 5–10 multiple choice questions.
    2) Each question must include:
       - question
       - 4 options
       - correct answer (must exactly match one option)
       - difficulty (easy | medium | hard)
       - explanation grounded in article text

    3) Extract:
       - short summary (3–4 sentences)
       - key entities grouped as:
            people
            organizations
            locations
       - major section titles mentioned in the text

    4) Suggest 3–6 related Wikipedia topics based ONLY on themes appearing in the article.

    OUTPUT FORMAT (STRICT JSON):
    {{
      "url": "{url}",
      "title": "Extract Title from text",
      "summary": "Summary text...",
      "key_entities": {{
        "people": [],
        "organizations": [],
        "locations": []
      }},
      "sections": [],
      "quiz": [
        {{
          "question": "Question text",
          "options": ["Op1", "Op2", "Op3", "Op4"],
          "answer": "Op1",
          "difficulty": "easy",
          "explanation": "Explanation..."
        }}
      ],
      "related_topics": []
    }}
    """

    headers = {
      "Authorization": f"Bearer {api_key}",
      "Accept": "application/json",
      "Content-Type": "application/json"
    }

    payload = {
      "model": "meta/llama-4-maverick-17b-128e-instruct",
      "messages": [{"role":"user","content": prompt}],
      "max_tokens": 2048, # Increased to accommodate full JSON response
      "temperature": 0.7,
      "top_p": 1.00,
      "stream": False
    }

    try:
        response = requests.post(invoke_url, headers=headers, json=payload)
        response.raise_for_status()
        
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        
        # Clean response content to ensure it's valid JSON
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        content = content.strip()
        
        return json.loads(content)
        
    except Exception as e:
        print(f"Error generating quiz: {e}")
        if hasattr(e, 'response') and e.response is not None:
             print(f"Response text: {e.response.text}")
        raise Exception(f"Failed to generate quiz with NVIDIA API: {str(e)}")
