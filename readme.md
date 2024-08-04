<h1 align="center">
    Rei
</h1>

<h4 align="center">Node for UniCheckBot</h4>

## Launguage
[Russian](readme_ru.md) | [English](readme.md)

## Why?
* UniCheck has a distributed model, to perform checks from different locations. 
* The bot sends a request to the nodes that perform checks. After that, check result will be returned to bot.

## Tech stack?
* It uses python 3.9 and Starlette.

## What checks can node do?
* HTTP checks, ping and status-code
* ICMP checks, jitter and RTT
* TCP port and service on it (very WIP)
* Check for Minecraft server - core version, ping, player and other info
* Check for SPTarkov server - mods, game version...
* Check for servers that uses Valve's Server Query Protocol (Half-Life 2, Half-Life, Team Fortress 2, Counter-Strike: Global Offensive, Counter-Strike 1.6, ARK: Survival Evolved, Rust and more)
* Check for Vintage story server - at now it get info from master-server.

## Installing
0. Write to [me](https://t.me/kiriharu) to obtain server token. Without the token, node will not be used in bot.
1. Install docker and docker-compose.
2. Clone git repo:

```
git clone https://github.com/unicheckbot/rei
```

3. Edit .env
```
PORT=33696 # service port
NODE_NAME=Default Unicheck Rei Node # name of your nde
NODE_TOWN=Undefined # Town, where node located
NODE_COUNTRY=Location # Country, where node located
ANNOUNCE_SERVER_SECRET=GET_SECRET_FROM_ADMIN # Token what you can obtain in 1
```

4. Start it!
```
docker-compose up -d --build
```

5. Updates will provide automatically by watchtower 

