<h1 align="center">
    Rei
</h1>

<h4 align="center">Нода-чекер для UniCheckBot</h4>

## Зачем?
* У UniCheck "распределенная" модель проверок -- его основная задача получать проверки с различных ресурсов. Для получения статистик с различных локаций используются ноды -- бот посылает на них запросы, они производят проверки и возвращают результат боту.

## На чём написано?
* Используется Python 3.9, написано на Starlette.

## Какие проверки делает нода?
* HTTP проверки с возвратом пинга и статус-кода
* ICMP проверка с возвратом дополнительных данных в виде jitter и RTT
* Проверка Minecraft-сервера с возвратом небольшой статистики (используемое ядро, версия) и задержки
* Проверка доступности TCP порта с возможностью узнать, какой сервис на нём висит
* Проверка и получение данных о сервере имплементирующие Valve's Server Query Protocol (Half-Life 2, Half-Life, Team Fortress 2, Counter-Strike: Global Offensive, Counter-Strike 1.6, ARK: Survival Evolved, Rust)

## Установка
0. Просим у [меня](https://t.me/kiriharu) токен, который необходимо будет добавить далее. Без токена сервер не попадёт в список бота и его использование будет затруднено.
1. Ставим Docker и Docker-compose. Установку данных пакетов тут я приводить не буду, так как 
2. Клонируем репозиторий с sub-модулями:

```
git clone --recurse-submodules  https://github.com/unicheckbot/rei
```

3. Редактируем .env
```
PORT=33696 # порт сервиса
NODE_NAME=Default Unicheck Rei Node # имя вашей ноды
NODE_TOWN=Undefined # Город, в котором расположен сервер
NODE_COUNTRY=Location # Страна, в которой расположен ваш сервер
ANNOUNCE_SERVER_SECRET=GET_SECRET_FROM_ADMIN # Секрет, который я вам выдал в пункте 0
```

4. Запускаем
```
docker-compose up -d --build
```

5. Обновление 
```
cd rei/ # заходим в каталог с сервером
docker-compose down
git pull --recurse-submodules
docker-compose up -d
```