

import json

import requests


url = "http://localhost:11434/api/generate"

model = "llama3.2"

data = {"prompt": "Tell me why is sky blue in short, like one sentence only",
        "model": "llama3.2",
        "stream": True}

response = requests.post(url, json=data)
# print(response.json()["response"])


for line in response.iter_lines():
    decode = (line.decode('utf-8'))
#     print(decode)
    dictionary = json.loads(decode) 
    print(dictionary["response"])


