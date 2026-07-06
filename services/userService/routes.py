from fastapi import APIRouter
import asyncio
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/login")
async def login():
    await asyncio.sleep(4)
    return {
        "message": "Login Successful"
    }


@router.get("/allUsers")
async def get_users():
    await asyncio.sleep(4)
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

@router.get("/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": f"User {user_id}"
    }


