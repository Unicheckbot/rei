import os
import secrets

# APP PORT
APP_PORT = os.environ.get("PORT", 33696)

# Node name.
NODE_NAME = os.environ.get("NODE_NAME", "Default node")

# Node location. Will be shown in tgbot
NODE_TOWN = os.environ.get("NODE_TOWN", "Undefined")
NODE_COUNTRY = os.environ.get("NODE_COUNTRY", "Location")

# Secret key for announce server. Should be requested.
ANNOUNCE_SERVER_SECRET = os.environ.get("ANNOUNCE_SERVER_SECRET", "GET_SECRET_FROM_ADMIN")
ANNOUNCE_SERVER_URL = os.environ.get("ANNOUNCE_SERVER_URL", "https://unicheck.kiriha.ru")

# Is icmp requests privileged. Some users need to host Rei instance outside docker without root access.
# Set this variable to 0 (False) if you want to run icmp requests unprivileged
ICMP_PRIVILEGED = int(os.environ.get("ICMP_PRIVILEGED", True))

# DON'T CHANGE LINES BELOW
TOKEN = secrets.token_urlsafe(32)
VERSION = "0.4.2"
NAME = "Rei"

DEBUG = int(os.getenv("DEBUG", 1))

METHODS_COUNTER = {
    "http": 0,
    "icmp": 0,
    "minecraft": 0,
    "tcp": 0,
    "source": 0,
    "spt": 0,
    "vintagestory": 0
}

INFO = {
    "stats": METHODS_COUNTER,
    "version": VERSION,
    "server": NAME,
    "server_name": NODE_NAME,
    "town": NODE_TOWN,
    "country": NODE_COUNTRY,
    "port": APP_PORT
}
