Prompt Template for Quiz Generation:

"""
You are an expert quiz generator and knowledge extractor.
Your task is to create a high-quality quiz ONLY from the provided Wikipedia article text.

STRICT RULES:
- Use only the provided article content
- Do NOT use outside knowledge
- Do NOT hallucinate facts not present in the text
- If something is unclear, skip it
- Questions must be fact-based and verifiable from the article
- Ensure answer correctness
- Distribute difficulty across easy, medium, and hard
- Avoid trick questions
- Avoid ambiguous answers
- Each explanation must reference where the answer appears (section or topic)
- Output MUST be valid JSON only

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

5) Questions must:
   - cover different parts of the article
   - not repeat the same fact
   - include at least:
        2 easy
        2 medium
        1 hard question

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

Return ONLY raw JSON. Do not use markdown code blocks.
"""
