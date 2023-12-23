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

Проект использует PostgreSQL в качестве БД, запуск в Docker-контейнере:

```
cd backend
docker build -t foodgram_backend .
docker run --name foodgram_backend_container --rm -p 8000:8000 foodgram_backend
```