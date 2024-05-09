import requests
import logging

from .config import (
    ANNOUNCE_SERVER_URL, APP_PORT, ANNOUNCE_SERVER_SECRET, TOKEN, DEBUG
)
from .utils import run_in_eventloop


class BadRequestForAPI(Exception):
    pass


logger = logging.getLogger("uvicorn.info")


async def register_node() -> None:
    if DEBUG:
        logger.info(f"Token: {TOKEN}")
    logger.info("Registering or updating node on API server...")
    try:
        # pls notice me to rewrite this shit to httpx or other async http lib...
        def register() -> requests.Response:
            data = requests.post(
                f"{ANNOUNCE_SERVER_URL}/api/register",
                json=dict(
                    port=APP_PORT,
                    api_token=TOKEN,
                    access_token=ANNOUNCE_SERVER_SECRET
                )
            )
            return data

        resp: requests.Response = await run_in_eventloop(register)
        if resp.status_code == 400:
            logger.error(f"Error registering on API server: {resp.json()}")
        else:
            if resp.json()['message'] == "Node created":
                logger.info("Server registered successfully")
            if resp.json()['message'] == "Node updated":
                logger.info("Server status updated successfully")
    except Exception as e:
        logger.error(f"Other exception has been occurred in register node process: {e}")
