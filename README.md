# CarValuationService

|                  |                                                   |
|------------------|---------------------------------------------------|
| Название команды | **TopGear**                                       |
| Состав команды   | Александр Рыжков<br>Максим Хатин<br>Иван Литвинов |
| Название проекта | **Улучшение оценки стоимости авто**               |

## Запуск
`git clone -b dev https://github.com/Sinus2x/CarValuationService.git` <br />
`cd ./CarValuationService` <br />
`docker volume create --name=grafana-volume` <br />
`docker-compose up -d`

Сервис доступен по http://0.0.0.0:8000/docs, где во вкладке `/predict` можно протестировать запрос на оценку стоимости машины.
Примеры запросов есть в [experiments/car_inference_test.txt](experiments/car_inference_test.txt)

| Название | Адрес                    |
|----------|--------------------------|
| Сервис   | http://0.0.0.0:8000/docs |
| Локуст   | http://0.0.0.0:8089      |
| Графана  | http://0.0.0.0:3000      |

## Структура репозитория


| Название папки                                   | Значение                                                                |
|--------------------------------------------------|-------------------------------------------------------------------------|
| [car_valuation_service](car_valuation_service/)  | Код сервиса                                                             |
| [eda](eda/)                                      | Ноутбуки с EDA                                                          |
| [experiments](experiments/)                      | Ноутбуки с обучением модели                                             |
| [metrics](metrics/)                              | Обоснование выбора метрик и схема решения                               |
| [motivation](motivation/)                        | Оценка проекта до взятия в работу                                       |
