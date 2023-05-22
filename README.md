# CarValuationService

1. **TopGear** - название команды
2. Александр Рыжков, Максим Хатин, Иван Литвинов - состав команды
3. **Улучшение оценки авто** - название проекта

## Запуск
`git clone https://github.com/Sinus2x/CarValuationService.git` <br />
`cd ./CarValuationService` <br />
`docker volume create --name=grafana-volume` <br />
`docker-compose up -d`

Сервис доступен по https://0.0.0.0:8000/docs, где во вкладке `/predict` можно протестировать запрос на оценку стоимости
машины.


