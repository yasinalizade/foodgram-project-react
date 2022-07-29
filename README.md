# Diploma project - FOODgram
![example workflow](https://github.com/yasinalizade/foodgram-project-react/actions/workflows/main.yml/badge.svg)


### Описание

<p>
  Веб-сайт c кулинарными рецептами. Анонимный пользователь может просматривать рецепты, также для всех доступна фильтрация по тегам. Если пользователь авторизован он может просматривать рецепты других авторов, а также добавлять риецепты в корзину с возможностью скачать список необходимых продуктов в PDF-формате. Доступна подписка на других авторов и отметка рецептов, для просмотра на странице "Избранное".
</p>
### Где посмотреть
<p>
 URL : http://84.201.143.39

 Логин и пароль для админа
 
 username: admin
 
 password: admin
</p>
  
### Как запустить на своей машине 
Для запуска у вас должен быть установлен Docker и Docker-Compose

Клонировать репозиторий и перейти в папку infra 
```
git clone git@github.com:yasinalizade/foodgram-project-react.git
cd foodgram-project-react/infra
```
Запустить Docker
```
sudo docker compose up -d
```
Для работы приложения нужно выполнить миграции, добавить ингредиенты.
И собрать статические файлы.
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py load_ingredients
docker-compose exec web python manage.py collectstatic --no-input

```
После этого приложение будет доступно по адресу http://localhost/



Stack:

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=REST%20API)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/en/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex)](https://cloud.yandex.ru/)

#### Автор: <a href="https://github.com/yasinalizade/">Ясин Ализаде</a>
