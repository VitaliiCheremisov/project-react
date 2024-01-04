### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/VitaliiCheremisov/foodgram-project-react.git
```

```
cd backend
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```
Для запуска проекта локально c БД sqlite3:
1) В корневом каталоге создать .env файл
2) Описать переменные:
  SECRET_KEY="'<ваш SECRET_KEY>'"
  * Например SECRET_KET="'django-insecure-k21i13@3f^h'"
  ALLOWED_HOSTS="'<ваши ALLLOWED_HOSTS>'"'
  * Например ALLOWED_HOSTS="'localhost,web,127.0.0.1''"
```
cd backend
python3 manage.py runserver
```

Для запуска в Docker-контейнере с БД PostgreSQL:
1) В корневом каталоге создать .env файл
2) Описать переменные:
  SECRET_KEY=<>
  ALLOWED_HOSTS=<>
  ENGINE=<>
  POSTGRES_DB=<>
  POSTGRES_USER=<>
  POSTGRES_PASSWORD=<>
  DB_NAME=<>
  DB_HOST=<>
  DB_PORT=<>
```
cd backend
docker build -t foodgram_backend .
docker run --name foodgram_backend_container --rm -p 8000:8000 foodgram_backend
```