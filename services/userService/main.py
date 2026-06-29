from fastapi import FastAPI 
app=FastAPI()

@app.get("/")
def home():
    return {
        "service":"user service",
        "message":"Running successfully"
    }

@app.get("/health")
def health():
    return{
        "status":"healthy"
    }

@app.get("/users")
def get_users():
    return [
        {
            "id": 1,
            "name": "Alice"
        },
        {
            "id": 2,
            "name": "Bob"
        }
    ]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": f"User {user_id}"
    }


@app.post("/users/login")
def login():
    return {
        "message": "Login Successful"
    }



