# Load Testing Project

Нагрузочное тестирование с JMeter, WireMock, InfluxDB и Grafana.

## Что внутри

- **JMeter** — генератор нагрузки
- **WireMock** — заглушка тестируемого сервиса
- **InfluxDB** — хранение метрик
- **Grafana** — визуализация результатов
- **Docker Compose** — всё поднимается одной командой

## Как запустить

### 1. Требования

- Docker Desktop
- JMeter 5.5+
- Java 17

### 2. Поднять стенд

cd docker
docker-compose up -d

### 3. Проверить WireMock

Открыть в браузере: http://localhost:8080/hello

Ожидаемый ответ: Hello from WireMock!

### 4. Проверить Grafana

Открыть: http://localhost:3000

- Логин: admin
- Пароль: admin

### 5. Запустить тест

jmeter -n -t test-plan.jmx -l report/result.jtl -e -o report/html

### 6. Смотреть графики

В Grafana импортировать дашборд 5496 (JMeter Dashboard).

Или открыть HTML-отчёт:

open report/html/index.html

## Структура проекта

- docker/docker-compose.yml — WireMock + InfluxDB + Grafana
- wiremock/mappings/hello.json — заглушка для GET /hello
- data/users.csv — тестовые данные
- test-plan.jmx — сценарий JMeter
- report/ — результаты тестов

## Как остановить

cd docker
docker-compose down

## Результаты тестирования

Тест: CRUD сценарий (POST → GET → PUT → DELETE) с использованием WireMock.

| Метрика | Значение |
| :--- | :--- |
| Профиль нагрузки | 100 пользователей за 120 секунд, 10 циклов |
| Всего запросов | 4000 |
| Пиковый Throughput | 40 req/s |
| Средний Throughput | 33 req/s |
| 95-й процентиль времени ответа | 3 мс |
| Ошибки | 0 |

Вывод: система работает стабильно, узких мест не выявлено. Время ответа находится в пределах SLA (500 мс) с большим запасом.
