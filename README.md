### Описание проекта:
YaMDB - социальная сеть, позволяющая делиться с другими пользователями обзорами художественных произведений и выставлением оценок, а также комментировать обзоры других пользователей.
В настоящее время функционал реализован через программный интерфейс приложения (API). Формат передачи данных - объектная запись JavaScript (JSON).


![Status of build](https://github.com/qwantilium/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master)

ip server 51.250.28.160

Что можно делать???
1. Получать список категорий (/api/v1/categories/). Если вы администратор, можно добавлять новые.
2. Получать список жанров (/api/v1/genres/). Если вы администратор, можно добавлять новые.
3. Получать список произведений (/api/v1/titles/). Если вы администратор, можно добавлять новые, заменять, обновлять, удалять существующие. (/api/v1/titles/{id}/)
4. Получать список обзоров. Если вы зарегистрированный пользователь, можно создавать свой обзор. (/api/v1/titles/{id}/reviews/).
5. Если вы автор обзора, можно его обновить, заменить, удалить. Это могут делать также администраторы и модераторы. (/api/v1/titles/{id}/reviews/{id}/)
6. Получать список комментариев к обзору. Если вы зарегистрированный пользователь, можно прокомментировать обзор. (/api/v1/titles/{id}/reviews/{id}/comments/).
7. Если вы автор комментария, можно его обновить, заменить, удалить. Это могут делать также администраторы и модераторы. (/api/v1/titles/{id}/reviews/{id}/comments/{id}/)
8. Если вы не зарегистрированы в социальной сети, вы можете это сделать, отправив email и username (/api/v1/auth/signup/). Далее отправить POST-запрос с параметрами username и confirmation_code (/api/v1/auth/token/). В ответе на запрос получить token.
9. Получить список всех пользователей, добавить нового пользователя, если вы администратор. (/users/)
10. Получить информацию по конкретному пользователю, обновить информацию или удалить пользователя, если вы администратор. (/user/{username}/)
11. Если вы зарегистрированный пользователь, вы можете получить о себе информацию, а также обновить ее. (/user/me/)


3. Получать список сообществ. (/api/v1/groups/)
4. Получать описание каждого сообщества. (/api/v1/groups/{id}/)
5. Получать список комментариев к посту. Создавать свой пост. (/api/v1/posts/{id}/comments/)
6. Получать конкретный комментарий. Если это комментарий пользователя, можно его изменять и удалять. (/api/v1/posts/{id}/comments/{id}/)
7. Смотреть, на кого вы подписаны. Подписываться на других пользователей. (/api/v1/follow/)

Запросы на чтение за исключением п.7 доступны анонимным пользователям.

### Шаблон .env файла:
```
DB_ENGINE='СУБД на выбор'
DB_NAME='Имя базы данных'
POSTGRES_USER='имя пользователя'
POSTGRES_PASSWORD='пароль пользователя'
DB_HOST='хост'
DB_PORT='порт'
```
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/qwantilium/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
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

Запустить проект:

```
python3 manage.py runserver
```
### Запуск приложения в конейнере ТУТОРИАЛ
Создать образ приложения ИЗ КОРНЯ ПРОЕКТА:
```
docker build -t 'название образа' .
```
Собрать и запустить все образы вместе с NGINX и GUNICORN:
```
docker-compose up -d --build
```
Теперь проект доступен по адресу http://127.0.0.1/

Остановить все образы:
```
docker-compose up
```

### Собрать и заполнить базу данных
Выполните миграции.
```
docker-compose exec web python manage.py migrate --noinput
```
Создайте суперпользователя.
```
docker-compose exec web python manage.py createsuperuser
```
Собрать статику
```
docker-compose exec web python manage.py collectstatic --no-input 
```
Войдите в админку по адресу http://127.0.0.1/admin/
Создайте одну-две записи объектов.

Создать резервную копию базы данных
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```

### Примеры

Получение произведений (запрос - ответ):

```
/api/v1/titles/
```

```JSON
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```

Создание обзора (запрос - содержание - ответ):

```
/api/v1/title/{id}/reviews/
```

```JSON
{
  "text": "string",
  "score": 1
}
```

```JSON
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```

Получение публикации по id (запрос - ответ):

```
/users/
```

```JSON
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
