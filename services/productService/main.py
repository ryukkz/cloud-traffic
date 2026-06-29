from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "service": "Product Service",
        "message": "Running Successfully"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/products")
def get_products():
    return [
        {
            "id": 1,
            "name": "Laptop",
            "price": 75000
        },
        {
            "id": 2,
            "name": "Phone",
            "price": 35000
        }
    ]