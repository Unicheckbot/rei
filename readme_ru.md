<h1 align="center">
    Rei
</h1>

<h4 align="center">Нода для UniCheckBot</h4>

## Язык
[Russian](readme_ru.md) | [English](readme.md)

## Почему?
* UniCheck имеет распределенную модель, позволяющую выполнять проверки из разных мест. 
* Бот отправляет запрос на узлы, которые выполняют проверку. После этого результат проверки будет возвращен боту.

## Стек?
* Используется Python 3.9 и Starlette

## Какие проверки может провести нода?
* Проверка HTTP с возвратом ping и status-code
* Проверки ICMP с возвратом jitter и RTT
* Проверка TCP порта и сервиса на нем (всё ещё WIP)
* Проверка Minecraft сервера - версия ядра, количество игроков, и так далее
* Проверка сервера SPTarkov - моды, версия игры и так далее
* Проверка серверов которые используют Valve's Server Query Protocol (Half-Life 2, Half-Life, Team Fortress 2, Counter-Strike: Global Offensive, Counter-Strike 1.6, ARK: Survival Evolved, Rust и другие)
* Проверка сервера Vintage story server - сейчас информация получается с master-сервера

## Установка
0. Напишите [мне](https://t.me/kiriharu) чтобы получить токен. Без токена, бот не сможет получить ноду.
1. Установите docker и docker-compose.
2. Скопируйте git репозиторий:

```
git clone https://github.com/unicheckbot/rei
```

3. Измените .env
```
PORT=33696 # Порт сервиса
NODE_NAME=Default Unicheck Rei Node # Имя ноды
NODE_TOWN=Undefined # Город, где расположена нода
NODE_COUNTRY=Location # Страна, где расположена нода
ANNOUNCE_SERVER_SECRET=GET_SECRET_FROM_ADMIN # Токен, который вы получили в пункте 1
```

4. Запустите!
```
docker-compose up -d --build
```

5. Обновляется нода автоматически при помощи watchtower.

