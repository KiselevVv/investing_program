# Investing program

## Описание

Сервис, который поможет инвесторам провести фундаментальный анализ на основе отчетов компании и оценить ее эффективность. 
С помощью него вы сможете выбрать лучшую компанию в отрасли и решить, покупать ее акции или нет.

## Стек технологий

- Python
- Flask
- SQLAlchemy
- Docker

## Для запуска через Docker:
 
- Cоберите образ:

`docker build -t invest .`

- Запустите контейнер:

`docker run -p 8080:5000 invest`

Проект будет доступен по адресу http://localhost:8080/

## Для запуска локально:

- Cоздать и активировать виртуальное окружение:

`python -m venv venv`

`source venv/Scripts/activate`

- Установить зависимости из файла requirements.txt:

`python -m pip install --upgrade pip`

`pip install -r requirements.txt`

- Запустить проект:

`python run.py`

## Пример:

Тестовый csv файл находится в папке 'csv'

## Автор:

Киселев Влад