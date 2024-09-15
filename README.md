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
- /auth/register \\
Request:
```json
{
  "username": "example",
  "password": "example"
}
```
- /auth/login \\
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

- /notes/create/
- /notes/list/
- /notes/update/:note_id/
- /notes/delete/:note_id/
- /notes/search_by_tags/
- /notes/search_by_title/
  
