import requests

# api = "https://opossum-accurate-chipmunk.ngrok-free.app"
api = "http://localhost:8009"
url = f"{api}/api/llm/"
data = {"question": input("Запрос: ")}

response = requests.post(url, json=data)
print(response.json())
