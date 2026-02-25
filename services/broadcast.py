import json
import os
from typing import Dict, List, Optional
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

USERS_FILE = 'data/users.json'


def init_users_file():
    """Ініціалізація файлу з користувачами"""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=4)


def save_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None):
    """Збереження користувача у файл"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}

    user_id_str = str(user_id)
    if user_id_str not in users:
        users[user_id_str] = {
            'user_id': user_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'subscribed': True,
            'first_seen': str(import_datetime().now()),
            'last_activity': str(import_datetime().now())
        }
    else:
        users[user_id_str]['last_activity'] = str(import_datetime().now())
        if username:
            users[user_id_str]['username'] = username

    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


def import_datetime():
    """Імпорт datetime для уникнення циркулярних імпортів"""
    from datetime import datetime
    return datetime


def get_all_users() -> List[Dict]:
    """Отримання всіх користувачів"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)
            return list(users.values())
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_subscribed_users() -> List[Dict]:
    """Отримання підписаних користувачів"""
    users = get_all_users()
    return [user for user in users if user.get('subscribed', True)]


def get_user_count() -> Dict[str, int]:
    """Отримання статистики користувачів"""
    users = get_all_users()
    subscribed = sum(1 for user in users if user.get('subscribed', True))

    return {
        'total': len(users),
        'subscribed': subscribed,
        'unsubscribed': len(users) - subscribed
    }


def unsubscribe_user(user_id: int) -> bool:
    """Відписка користувача від розсилки"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)

        user_id_str = str(user_id)
        if user_id_str in users:
            users[user_id_str]['subscribed'] = False

            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
            return True
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return False


def get_confirmation_keyboard(broadcast_id: str) -> InlineKeyboardMarkup:
    """Створення клавіатури для підтвердження розсилки"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Підтвердити",
                callback_data=f"confirm_broadcast:{broadcast_id}"
            ),
            InlineKeyboardButton(
                text="❌ Скасувати",
                callback_data=f"cancel_broadcast:{broadcast_id}"
            )
        ]
    ])
    return keyboard

def get_subscribed_users_count() -> int:
    """Отримання кількості підписаних користувачів"""
    return len(get_subscribed_users())