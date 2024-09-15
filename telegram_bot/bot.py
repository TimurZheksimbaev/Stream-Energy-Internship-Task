from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.fsm.state import State
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from config import TELEGRAM_BOT_TOKEN
from logger import logger
from api_client import get_notes, create_note, search_notes_by_tags, login_user, search_notes_by_title
from aiogram import F

from aiogram.fsm.state import StatesGroup, State
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

user_data = {}
user_tokens = {}

""""""""""""""""""""""""" Start Bot """""""""""""""

@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    user_data[message.from_user.id] = {
        "telegram_username": message.from_user.username
    }
    await dp.throttle(key=f"start_{message.from_user.id}", rate=3)
    logger.info(f"User {message.from_user.username} started bot")
    await message.reply(f"Привет, {message.from_user.username}! Добро пожаловать в бот заметок.")



"""""""""""""""" Login """""""""""""""""
class LoginState(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()


@dp.message(Command(commands=["login"]))
async def login(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше имя пользователя.")
    await state.set_state(LoginState.waiting_for_username)

# Получение имени пользователя
@dp.message(LoginState.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Введите ваш пароль.")
    await state.set_state(LoginState.waiting_for_password)

# Получение пароля и завершение логина
@dp.message(LoginState.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    username = data['username']
    password = message.text

    # Пытаемся авторизоваться через API
    token = await login_user(username, password)
    if token:
        user_tokens[message.from_user.id] = token  # Сохраняем токен для пользователя
        await message.answer("Авторизация успешна!")
        await state.clear()  # Очищаем состояние после успешной авторизации
    else:
        await message.answer("Неверные данные для входа. Попробуйте еще раз.")
        await state.clear()  # Очищаем состояние в случае неудачи, чтобы не застрять




""""""""""""""""""""""""""""""" Create note """""""""""""""""""""""""""""""""

class NoteCreation(StatesGroup):
    waiting_for_title = State()
    waiting_for_content = State()
    waiting_for_tags = State()

@dp.message(Command(commands=["new_note"]))
async def create_new_note_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    token = user_tokens.get(user_id)

    if not token:
        await message.answer("Вы не авторизованы. Пожалуйста, выполните вход с помощью команды /login.")
        return

    await message.answer("Пожалуйста, отправьте заголовок заметки.")
    await state.set_state(NoteCreation.waiting_for_title)


# Получение заголовка заметки
@dp.message(NoteCreation.waiting_for_title)
async def get_note_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)  # Сохраняем заголовок во временные данные FSM
    await message.answer("Теперь отправьте содержание заметки.")
    await state.set_state(NoteCreation.waiting_for_content)


# Получение содержания заметки
@dp.message(NoteCreation.waiting_for_content)
async def get_note_content(message: Message, state: FSMContext):
    await state.update_data(content=message.text)  # Сохраняем содержание во временные данные FSM
    await message.answer("Отправьте теги для заметки через запятую.")
    await state.set_state(NoteCreation.waiting_for_tags)


# Получение тегов и создание заметки
@dp.message(NoteCreation.waiting_for_tags)
async def get_note_tags(message: Message, state: FSMContext):
    user_id = message.from_user.id
    token = user_tokens.get(user_id)
    tags = [str(tag.strip()) for tag in message.text.split(',')]

    # Получаем данные из состояний
    data = await state.get_data()
    title = data['title']
    content = data['content']

    try:
        # Взаимодействие с API для создания заметки
        note = await create_note(user_id, title, content, tags, token)
        await message.answer(f"Заметка '{note['title']}' успешно создана.")
    except Exception as e:
        logger.error(f"Error creating note: {str(e)}")
        await message.answer("Произошла ошибка при создании заметки.")

    await state.clear()  # Очищаем состояние после завершения процесса




""""""""""""""""""""""""""""" Get notes """""""""""""""""""""""

@dp.message(Command(commands=["notes"]))
async def get_user_notes(message: types.Message):
    user_id = message.from_user.id
    token = user_tokens.get(user_id)

    if not token:
        await message.answer("Вы не авторизованы. Пожалуйста, выполните вход с помощью команды /login.")
        return

    try:
        notes = await get_notes(user_id, token)
        if notes:
            response = "\n\n".join([f"Заголовок: {note['title']}\nТеги: {', '.join(note['tags'])}\nСодержание: {note['content']}" for note in notes])
        else:
            response = "У вас пока нет заметок."
        await message.answer(response)
    except Exception as e:
        logger.error(f"Error fetching notes: {str(e)}")
        await message.answer("Произошла ошибка при получении заметок.")


""""""""""""""""""""""""""""""" Search notes by tag """""""""""""""""""""""""
class SearchByTags(StatesGroup):
    waiting_for_tags = State()

@dp.message(Command(commands=["search_note_by_tags"]))
async def search_note_by_tags(message: types.Message, state: FSMContext):
    await message.answer("Введите теги для поиска заметок, разделяя их запятыми.")
    await state.set_state(SearchByTags.waiting_for_tags)

@dp.message(SearchByTags.waiting_for_tags)
async def get_notes_by_tags(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    tags = [tag.strip() for tag in message.text.split(',')]
    token = user_tokens.get(user_id)

    if not token:
        await message.answer("Вы не авторизованы. Пожалуйста, выполните вход с помощью команды /login.")
        await state.clear()
        return

    try:
        notes = await search_notes_by_tags(user_id, tags, token)
        if notes:
            response = "\n\n".join([f"Заголовок: {note['title']}\nТеги: {', '.join(note['tags'])}\nСодержание: {note['content']}" for note in notes])
        else:
            response = f"Заметок с тегами '{', '.join(tags)}' не найдено."
        await message.answer(response)
    except Exception as e:
        logger.error(f"Error searching notes by tags: {str(e)}")
        await message.answer("Произошла ошибка при поиске заметок.")
    finally:
        await state.clear()




"""""""""""""""""""""" Search notes by title """""""""""""""""""""""

class SearchByTitle(StatesGroup):
    waiting_for_title = State()

@dp.message(Command(commands=["search_note_by_title"]))
async def search_note_by_title(message: types.Message, state: FSMContext):
    await message.answer("Введите заголовок для поиска заметок.")
    await state.set_state(SearchByTitle.waiting_for_title)


@dp.message(SearchByTitle.waiting_for_title)
async def get_notes_by_title(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    title = message.text.strip()
    token = user_tokens.get(user_id)

    if not token:
        await message.answer("Вы не авторизованы. Пожалуйста, выполните вход с помощью команды /login.")
        await state.clear()
        return

    try:
        notes = await search_notes_by_title(user_id, title, token)
        if notes:
            response = "\n\n".join(
                [f"Заголовок: {note['title']}\nТеги: {', '.join(note['tags'])}\nСодержание: {note['content']}" for note
                 in notes])
        else:
            response = f"Заметок с заголовком '{title}' не найдено."
        await message.answer(response)
    except Exception as e:
        logger.error(f"Error searching notes by title: {str(e)}")
        await message.answer("Произошла ошибка при поиске заметок.")
    finally:
        await state.clear()


async def main():
    await dp.start_polling(bot)


# Запуск бота
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
