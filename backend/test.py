import requests

url = "http://127.0.0.1:8000/chat/stream"

payload = {
    "messages": [
        {"role": "user", "content": "What is FastAPI?"}
    ]
}

with requests.post(url, json=payload, stream=True) as r:
    for chunk in r.iter_content(chunk_size=None):
        if chunk:
            print(chunk.decode(), end="")
