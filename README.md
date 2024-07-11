# Sport-Calendar-API

## Description

This is a simple API that allows you to get a list of sports events for a given date. The API is built using FastAPI and
uses the [SQLite](https://www.sqlite.org/) API to get the sports events.

## Installation

To install the API, you need to have Python 3.7 or higher installed on your machine along with poetry.

Clone the repository:

 ```bash
git clone url 
```

Install the dependencies:

```bash
poetry install
```

Run the API:

```bash
poetry run uvicorn sport_calendar_api.main:app --reload
```
