from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "service": "Order Service",
        "message": "Running Successfully"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/orders")
def get_orders():
    return [
        {
            "order_id": 1001,
            "user_id": 1,
            "amount": 500
        },
        {
            "order_id": 1002,
            "user_id": 2,
            "amount": 1500
        }
    ]