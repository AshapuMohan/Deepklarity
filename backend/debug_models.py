import sys
print("Starting script...")
try:
    import os
    print("Imported os")
    import google.generativeai as genai
    print("Imported genai")
    from pathlib import Path
    from dotenv import load_dotenv
    print("Imported dotenv")

    env_path = Path(__file__).parent / '.env'
    print(f"Loading .env from {env_path}")
    load_dotenv(dotenv_path=env_path)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY not found.")
    else:
        print(f"API Key found: {api_key[:5]}...{api_key[-5:]}")
        genai.configure(api_key=api_key)
        
        print("Listing available models...")
        with open("backend/models_list.txt", "w", encoding="utf-8") as f:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"- {m.name}")
                    f.write(f"{m.name}\n")
        print("Written to backend/models_list.txt")
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
