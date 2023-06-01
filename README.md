# CarValuationService

|                  |                                                   |
|------------------|---------------------------------------------------|
| Название команды | **TopGear**                                       |
| Состав команды   | Александр Рыжков<br>Максим Хатин<br>Иван Литвинов |
| Название проекта | **Улучшение оценки авто**                         |

## Запуск
`git clone -b litvinov_load_testing_bench https://github.com/Sinus2x/CarValuationService.git` <br />
`cd ./CarValuationService` <br />
`docker volume create --name=grafana-volume` <br />
`docker-compose up -d`

Сервис доступен по http://0.0.0.0:8000/docs, где во вкладке `/predict` можно протестировать запрос на оценку стоимости машины.

| Название | Адрес                    |
|----------|--------------------------|
| Сервис   | http://0.0.0.0:8000/docs |
| Локуст   | http://0.0.0.0:8089      |
| Графана  | http://0.0.0.0:3000      |
