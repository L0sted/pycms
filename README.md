Здесь будет CMS на питоне с MongoDB.

DB: pythoncms
Table: posts
Format:
```
{
  "_id": "0123456789",
  "name": "Title",
  "text": "Hello, this is post"
}
```
Index page:

```
{
  "_id": "0123456789",
  "name": "/",
  "text": "Hello, this is index page"
}

```

# Routes:

GET /post — список статей.
GET /post/name — отдельная статья.
POST /admin/posts — создать статью.
PUT /admin/posts — обновить статью.
DELETE /admin/posts/:id — удалить статью.

Все маршруты, которые начинаются с «/admin» требуют аутентификацию пользователя. Для stateless-сервиса очень удобно использовать Basic-аутентификацию, т.к. каждый запрос содержит логин и пароль пользователя.

# TODO:

* Переписать маршруты под админку
* Добавить авторизацию
* Добавить конфигурацию