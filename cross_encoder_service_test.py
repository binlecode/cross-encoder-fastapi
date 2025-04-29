import requests

# API_URL = f"http://localhost:8000"
API_URL = f"http://34.86.129.157/cross-encoder"


url = f"{API_URL}/rank"
payload = {
    "query": "What is the capital of Germany?",
    "passages": [
        "Berlin is the capital of Germany.",
        "Munich is known for Oktoberfest.",
        "Frankfurt is a major financial center.",
        "Alice is a software engineer.",
        "Bob is a data scientist.",
        "Charlie is a product manager.",
        "Shanhai is a city in China.",
        "Beijing is the capital of China.",
        "Tokyo is the capital of Japan.",
        "Seoul is the capital of South Korea.",
        "Canberra is the capital of Australia.",
        "Ottawa is the capital of Canada.",
        "New Delhi is the capital of India.",
        "Brasilia is the capital of Brazil.",
        "Mexico City is the capital of Mexico.",
        "Buenos Aires is the capital of Argentina.",
    ],
    "top_k": 3,
}
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())
