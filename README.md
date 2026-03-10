# RedPanda DemoProject Operation Guide

## Basic Setup

1. Make sure you've installed Docker on your device. (<https://www.docker.com/>)
2. Navigate to the project root directory.
3. (Terminal) Run command `docker compose up -d`
4. (Terminal) Run command `uv sync`
5. (Terminal) Run command `uv run python3 manage.py migrate`
6. (Terminal) Run command `uv run python3 manage.py runserver`

## Create Topic

1. Open the Redpanda GUI in your browser! (<http://0.0.0.0:8080/overview>)
2. Click Topic in the sidebar
3. Create a topic (the settings are not important in this demo project — just enter your topic name and click Create!)
4. Go back to the project and open the file `demoproject/settings.py`
5. Change `REDPANDA_POCKETFAN_NAMELIST_TOPIC` to the topic name that you just created.

## [Producer] Put Data into RedPanda

1. Open the Swagger UI in your browser! (<http://127.0.0.1:8088/api/schema/swagger-ui>)
2. Use the API `/redpanda/demo-producer/` — Input data: `list[json, json...]`

Example:

```json
{
  "messages": [
        {
          "ino": "A123456789",
          "data": {
            "point": 12341234,
            "is_fan": false,
            "timestamp":"202603101056"
          }
        },
        {
          "ino": "B123456789",
          "data": {
            "point": 22342234,
            "is_fan": true,
            "timestamp":"202603101056"
          }
        }
  ]
}
```

## [Consumer] Get Data from API

1. Open the Swagger UI in your browser! (<http://127.0.0.1:8088/api/schema/swagger-ui>)
2. Use the API `/redpanda/demo-consumer/` — you will get all the data you put into RedPanda!

## [Consumer] Get Data from Django Command

1. (Terminal) Run command `uv run python3 manage.py consume_messages`
2. This command runs continuously until you press Ctrl+C to stop it!
3. Put data into RedPanda via the producer API and you will see it appear in the terminal in real time!
