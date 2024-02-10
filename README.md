# Дипломное задание, финальный проект
# Как работать с репозиторием дипломного задания

Проект foogram, работает в контейнерах Docker и имеет CI/CD GitHubActions

## Что нужно сделать

Склонировать репозиторий на ваш локальный компьютер
```
git clone https://github.com/VitaliiCheremisov/foodgram-project-react.git
```
Перейти в директорию проекта
```
cd foodgram-project-react
```
Создать .env файл для хранения переменных окружения в корневой директории проекта
Проект можно запустить локально с помощью Docker, находясь директории infra
```
docker-compose up
```
Запустить проект можно на удаленном серверe Docker
```
sudo docker-compose up -d
```
Выполнить миграции
```
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
```
Собрать статику
```
sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```
Заполнить базу данных рецептами
```
python3 manage.py import_csv ingredients.csv
```
При выполнении push в репозиторий GitHub настроены CI/CD c помощью GitHub Actions, проект тестируется,
образый пересобираются, заливаются на DockerHub, удаленный сервер скачивает их и передеплоит проект.

Технологии
```
Python 3.10
Django 3.2.3
Django REST framework 3.14
Nginx
Docker
Postgres
```

Автор
- [Виталий Черемисов](https://github.com/VitaliiCheremisov)