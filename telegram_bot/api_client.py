import aiohttp
from config import API_BASE_URL

async def login_user(username: str, password: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/auth/login/", json={"username": username, "password": password}) as response:
            if response.status == 200:
                data = await response.json()
                return data['access_token']  # Предполагаем, что API возвращает access_token
            else:
                return None

async def get_notes(user_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/notes/list/", headers=headers, params={"user_id": user_id}) as response:
            return await response.json()

async def create_note(user_id: int, title: str, content: str, tags: list[str], token: str):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_BASE_URL}/notes/create/", headers=headers, json={"title": title, "content": content, "tags": tags}) as response:
            return await response.json()

async def search_notes_by_tags(user_id: int, tags: list[str], token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/notes/search_by_tags/", headers=headers, json={"tags": tags}) as response:
            return await response.json()

async def search_notes_by_title(user_id: int, title: str, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/notes/search_by_title/", headers=headers, params={"title": title}) as response:
            return await response.json()
