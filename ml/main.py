import requests

api = "https://opossum-accurate-chipmunk.ngrok-free.app"
# api = "http://0.0.0.0:8009/"
url = f"{api}/api/llm/"
data = {"question": "Что такое PLAMO"}

response = requests.post(url, json=data)
print(response.json())
