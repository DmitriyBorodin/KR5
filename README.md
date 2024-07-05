# Парсинг ваканский с hh.ru

Эта программа написана на Python с использованием виртуального окружения Poetry, 
предназначена для сбора данных о вакансиях от интересующих пользователя компаний с сайта hh.ru. 
Полученные данные сохраняются в базу данных PostgreSQL.

## Установка

1. Скачайте модули проекта:
   
   ```
   git clone https://github.com/your_username/your_project.git
   ```

2. Установите Poetry, если у вас его еще нет:
   
   ```
   pip install poetry
   ```

3. Установите необходимые зависимости, указанные в файле pyproject.toml:
   
   ```
   poetry install
   ```

4. Создайте файл database.ini и укажите в нем параметры подключения к PostgreSQL, например:
   
   ```
   [postgresql]
   host=localhost
   user=postgres
   password=your_password
   port=5432
   ```

## Запуск

1. Запустите программу:
   
   ```
   poetry run python main.py
   ```

2. Программа начнет собирать данные о вакансиях от интересующих вас компаний с сайта hh.ru и сохранит их в базу данных.
