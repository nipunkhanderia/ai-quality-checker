import requests


ollama_base_url = "http://localhost:11434/api/generate"
ollama_model = "llama3.2"




payload = {
        "model":ollama_model,
        "prompt":"who is nipunkhanderia?",
        "stream":False
        }

response = requests.post(ollama_base_url, json=payload)

print(response.json()["response"])