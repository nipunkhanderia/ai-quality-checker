import requests


ollama_base_url = "http://localhost:11434/api/generate"
ollama_model = "llama3.2"


def call_ollama(prompt):
        payload = {
                "model":ollama_model,
                "prompt":prompt,
                "stream":False
                }
        response = requests.post(ollama_base_url, json=payload)
        # print(response.json()["response"])
        return response
