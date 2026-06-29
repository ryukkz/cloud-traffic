from fastapi import APIRouter

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get("/allOrders")
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