import requests

URL = "http://127.0.0.1:8000/users"

for i in range(15):
    response = requests.get(URL)
    print(f"Request {i+1}: {response.status_code}")