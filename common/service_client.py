from fastapi import FastAPI 
import httpx
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import asyncio
load_dotenv()
from common.config import (
    GATEWAY_URL,
    HEARTBEAT_INTERVAL
)

async def send_heartbeat(service_name, service_url):
    while True:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{GATEWAY_URL}/heartbeat",
                    json={
                        "service": service_name,
                        "url": service_url,"weight": 1
                    }
                )
            print("Heartbeat Sent")
        except Exception as e:
            print(e)

        await asyncio.sleep(HEARTBEAT_INTERVAL)

async def register(
    service_name,
    service_url
):
    wgt=int(input("enter weight: "))
    async with httpx.AsyncClient() as client:

        response = await client.post(
            f"{GATEWAY_URL}/register",
            json={
                "service": service_name,
                "url": service_url,
                "weight": wgt
            }
        )

        print(response.status_code)
        print(response.text)

    print(f"{service_name} registered")

async def unregister(
    service_name,
    service_url
):

    async with httpx.AsyncClient() as client:

        await client.post(
            f"{GATEWAY_URL}/unregister",
            json={
                "service": service_name,
                "url": service_url
            }
        )

    print(f"{service_name} unregistered")

def create_lifespan(
    service_name,
    service_url
):

    @asynccontextmanager
    async def lifespan(app):

        await register(
            service_name,
            service_url
        )

        heartbeat_task = asyncio.create_task(

        send_heartbeat(
                service_name,
                service_url
            )

        )

        yield

        heartbeat_task.cancel()

        # await unregister(
        #     service_name,
        #     service_url
        # )

    return lifespan