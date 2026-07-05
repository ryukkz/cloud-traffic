import requests

URL = "http://127.0.0.1:8000/users/allUsers"   # Your gateway endpoint

for i in range(20):
    response = requests.get(URL)
    print(f"Request {i+1}: {response.json()}")
     