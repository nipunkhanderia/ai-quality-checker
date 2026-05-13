import requests
import json


url = "http://localhost:11434/api/generate"
data = {
    "prompt": "Tell me why sky is blue in one sentence",
    "model": "llama3.2",
    "stream": True
    }

response = requests.post(url,"" ,data)
# print(response.json()["response"])

for line in response.iter_lines():
    decoded = line.decode("utf-8")
    cleaned_msg = json.loads(decoded)
    print(cleaned_msg["response"], end= " ")