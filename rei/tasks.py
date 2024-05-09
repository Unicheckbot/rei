import asyncio
import logging

from httpx import AsyncClient

from rei.config import (
    ANNOUNCE_SERVER_URL,
    APP_PORT,
    ANNOUNCE_SERVER_SECRET,
    TOKEN,
    DEBUG
)

logger = logging.getLogger("uvicorn.info")


async def register_node(client: AsyncClient) -> None:
    if DEBUG:
        logger.info(f"Token: {TOKEN}")
    while True:
        logger.info("Registering or updating node on API server...")
        try:
            resp = await client.post(
                f"{ANNOUNCE_SERVER_URL}/api/register",
                json=dict(
                    port=APP_PORT,
                    api_token=TOKEN,
                    access_token=ANNOUNCE_SERVER_SECRET
                )
            )
            data = resp.json()
            if resp.status_code == 400:
                logger.error(f"Error registering on API server: {data}")
            else:
                if data['message'] == "Node created":
                    logger.info("Server registered successfully")
                if data['message'] == "Node updated":
                    logger.info("Server status updated successfully")
        except Exception as e:
            logger.error(f"Other exception has been occurred in register node process: {e}")
        await asyncio.sleep(5)
