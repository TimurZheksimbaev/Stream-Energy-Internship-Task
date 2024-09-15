# Задание для Stream Energy

# Для запуска бэкенда
```bash
  uvicorn main:app --reload
```

# Для запуска бота 
```bash
  python telegram_bot/bot.py
```

# Бэкенд имеет следующие эндпоинты
- `/auth/register`\
Request:
```json
{
  "username": "example",
  "password": "example"
}
```
- `/auth/login`\
Request:
```json
{
  "username": "example",
  "password": "example"
}
```
Response:
```json
{
  "access_token": "qowieubcvtyowueb",
  "token_type": "bearer"
}
```

- `/notes/create/`\
Request:
```json
{
  "title": "example",
  "content": "exmaple",
  "tags": [
    "some",
    "tags"
  ]
}
```
- `/notes/list/`\
Response:
```json
[
  {
    "title": "example",
    "content": "exmaple",
    "tags": [
      "some",
      "tags"
    ]
  },
  ...
]
```
-
- `/notes/update/:note_id/`\
Request:
```json
{
  "title": "new_example",
  "content": "new_exmaple",
  "tags": [
    "new_some",
    "new_tags"
  ]
}
```
- `/notes/delete/:note_id/`\
- `/notes/search_by_tags/`\
  Request:
```json
{
  "tags": [
    "new_some",
    "new_tags"
  ]
}
```
- `/notes/search_by_title/`\
Request:
  some title
  
