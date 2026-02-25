import json
import os
import asyncio
import uuid

from aiogram import Bot, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from typing import Dict, Any, List

from services import admin_manager

# Словник для зберігання тимчасових даних розсилки
pending_broadcasts = {}
USERS_FILE = 'data/users.json'
router = Router()


def escape_html(text: str) -> str:
    """Екранує спеціальні символи HTML"""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def init_users_file():
    """Ініціалізація файлу користувачів"""
    os.makedirs('data', exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)


def save_user(user_id: int, username: str = None, first_name: str = None, last_name: str = None):
    """Збереження користувача"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)
    except:
        users = {}

    users[str(user_id)] = {
        'user_id': user_id,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'subscribed': True,
        'last_active': str(asyncio.get_event_loop().time())
    }

    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def get_subscribed_users() -> List[int]:
    """Отримання списку підписаних користувачів"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)

        subscribed = []
        for user_id, user_data in users.items():
            if user_data.get('subscribed', True):
                subscribed.append(int(user_id))
        return subscribed
    except:
        return []


def get_subscribed_users_count() -> int:
    """Кількість підписаних користувачів"""
    return len(get_subscribed_users())


def get_user_count() -> Dict[str, int]:
    """Статистика користувачів"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)

        total = len(users)
        subscribed = sum(1 for u in users.values() if u.get('subscribed', True))
        unsubscribed = total - subscribed

        return {
            'total': total,
            'subscribed': subscribed,
            'unsubscribed': unsubscribed
        }
    except:
        return {'total': 0, 'subscribed': 0, 'unsubscribed': 0}


def get_admin_main_keyboard() -> ReplyKeyboardMarkup:
    """Головна клавіатура адміністратора"""
    keyboard = [
        [KeyboardButton(text="📨 Нова розсилка")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="👥 Керування модераторами")],
        [KeyboardButton(text="❌ Вийти")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_broadcast_type_keyboard() -> ReplyKeyboardMarkup:
    """Клавіатура для вибору типу розсилки"""
    keyboard = [
        [KeyboardButton(text="📝 Текстова розсилка")],
        [KeyboardButton(text="🖼 Розсилка з фото")],
        [KeyboardButton(text="🎥 Розсилка з відео")],
        [KeyboardButton(text="🔙 Назад до адмінки")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_confirmation_keyboard(broadcast_id: str) -> InlineKeyboardMarkup:
    """Клавіатура підтвердження розсилки"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Підтвердити", callback_data=f"confirm_broadcast:{broadcast_id}"),
            InlineKeyboardButton(text="❌ Скасувати", callback_data=f"cancel_broadcast:{broadcast_id}")
        ]
    ])


async def send_broadcast_message(bot: Bot, text: str) -> Dict[str, int]:
    """Надсилання текстової розсилки"""
    users = get_subscribed_users()
    results = {
        'total': len(users),
        'successful': 0,
        'failed': 0,
        'blocked': 0
    }

    for user_id in users:
        try:
            # Використовуємо звичайний текст без HTML для безпеки
            await bot.send_message(chat_id=user_id, text=text, parse_mode=ParseMode.HTML)
            results['successful'] += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            error_str = str(e).lower()
            if 'blocked' in error_str or 'forbidden' in error_str:
                results['blocked'] += 1
            else:
                results['failed'] += 1

    return results


async def send_broadcast_message_with_photo(bot: Bot, text: str, photo_id: str) -> Dict[str, int]:
    """Надсилання розсилки з фото"""
    users = get_subscribed_users()
    results = {
        'total': len(users),
        'successful': 0,
        'failed': 0,
        'blocked': 0
    }

    for user_id in users:
        try:
            await bot.send_photo(
                chat_id=user_id,
                photo=photo_id,
                caption=text,
                parse_mode=ParseMode.HTML
            )
            results['successful'] += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            error_str = str(e).lower()
            if 'blocked' in error_str or 'forbidden' in error_str:
                results['blocked'] += 1
            else:
                results['failed'] += 1

    return results


async def send_broadcast_message_with_video(bot: Bot, text: str, video_id: str) -> Dict[str, int]:
    """Надсилання розсилки з відео"""
    users = get_subscribed_users()
    results = {
        'total': len(users),
        'successful': 0,
        'failed': 0,
        'blocked': 0
    }

    for user_id in users:
        try:
            await bot.send_video(
                chat_id=user_id,
                video=video_id,
                caption=text,
                parse_mode=ParseMode.HTML
            )
            results['successful'] += 1
            await asyncio.sleep(0.05)
        except Exception as e:
            error_str = str(e).lower()
            if 'blocked' in error_str or 'forbidden' in error_str:
                results['blocked'] += 1
            else:
                results['failed'] += 1

    return results


@router.message(Command("admin"))
async def admin_command(message: Message):
    """Команда для входу в адмін-панель"""
    if not admin_manager.is_admin(message.from_user.id):
        await message.answer("❌ У вас немає доступу до адмін-панелі!")
        return

    await message.answer(
        "👑 Ласкаво просимо до адмін-панелі!\n\n"
        "Оберіть дію:",
        reply_markup=get_admin_main_keyboard()
    )


@router.message(F.text == "📨 Нова розсилка")
async def new_broadcast_menu(message: Message):
    """Меню вибору типу розсилки"""
    if not admin_manager.is_admin(message.from_user.id):
        await message.answer("❌ Доступ заборонено!")
        return

    await message.answer(
        "📨 Створення нової розсилки\n\n"
        "Оберіть тип повідомлення:",
        reply_markup=get_broadcast_type_keyboard()
    )


@router.message(F.text == "📝 Текстова розсилка")
async def text_broadcast_start(message: Message):
    """Початок створення текстової розсилки"""
    if not admin_manager.is_admin(message.from_user.id):
        return

    await message.answer(
        "✏️ Текстова розсилка\n\n"
        "Надішліть текст для розсилки у відповідь на це повідомлення.\n\n"
        "Або використайте команду:\n"
        "/message Ваш текст"
    )


@router.message(F.text == "🖼 Розсилка з фото")
async def photo_broadcast_start(message: Message):
    """Початок створення розсилки з фото"""
    if not admin_manager.is_admin(message.from_user.id):
        return

    await message.answer(
        "🖼 Розсилка з фото\n\n"
        "Надішліть фото з підписом, починаючи з /photo\n\n"
        "Наприклад: надішліть фото з підписом:\n"
        "/photo Наше нове меню!"
    )


@router.message(F.text == "🎥 Розсилка з відео")
async def video_broadcast_start(message: Message):
    """Початок створення розсилки з відео"""
    if not admin_manager.is_admin(message.from_user.id):
        return

    await message.answer(
        "🎥 Розсилка з відео\n\n"
        "Надішліть відео з підписом, починаючи з /video\n\n"
        "Наприклад: надішліть відео з підписом:\n"
        "/video Новий ролик!"
    )


@router.message(F.text == "🔙 Назад до адмінки")
async def back_to_admin(message: Message):
    """Повернення до головного меню адмінки"""
    if not admin_manager.is_admin(message.from_user.id):
        return

    await message.answer(
        "👑 Головне меню адмін-панелі",
        reply_markup=get_admin_main_keyboard()
    )


@router.message(F.text == "❌ Вийти")
async def exit_admin(message: Message):
    """Вихід з адмін-панелі"""
    if not admin_manager.is_admin(message.from_user.id):
        return

    await message.answer(
        "👋 Ви вийшли з адмін-панелі.",
        reply_markup={"remove_keyboard": True}
    )


@router.message(F.text == "📊 Статистика")
async def stats_command(message: Message):
    """Статистика користувачів"""
    if not admin_manager.is_admin(message.from_user.id):
        await message.answer("❌ Ця команда тільки для адміністраторів!")
        return

    stats = get_user_count()

    total_users = stats['total']
    subscribed = stats['subscribed']
    unsubscribed = stats['unsubscribed']

    sub_percent = (subscribed / total_users * 100) if total_users > 0 else 0
    unsub_percent = (unsubscribed / total_users * 100) if total_users > 0 else 0

    await message.answer(
        f"📊 Статистика бота\n\n"
        f"👥 Користувачі:\n"
        f"• Всього: {total_users}\n"
        f"• Підписано: {subscribed} ({sub_percent:.1f}%) ✅\n"
        f"• Відписано: {unsubscribed} ({unsub_percent:.1f}%) ❌"
    )


@router.message(Command("message"))
async def broadcast_command(message: Message, bot: Bot):
    """
    Команда для розсилки повідомлень (тільки для адміністраторів)
    """
    if not admin_manager.can_edit(message.from_user.id):
        await message.answer("❌ Ця команда тільки для адміністраторів!")
        return

    # Отримуємо текст після команди
    text = message.text.replace('/message', '').strip()

    if not text:
        await message.answer(
            "✏️ Введіть текст для розсилки після команди /message\n"
            "Наприклад: /message Привіт всім!"
        )
        return

    # Створюємо унікальний ID для цієї розсилки
    broadcast_id = str(uuid.uuid4())

    # Зберігаємо дані розсилки
    pending_broadcasts[broadcast_id] = {
        'type': 'text',
        'text': text,
        'admin_id': message.from_user.id
    }

    # Відправляємо попередній перегляд (без HTML форматування)
    await message.answer(
        f"📨 ПОПЕРЕДНІЙ ПЕРЕГЛЯД РОЗСИЛКИ\n\n"
        f"Тип: Текст\n"
        f"Текст:\n{text}\n\n"
        f"👥 Отримають: {get_subscribed_users_count()} користувачів",
        reply_markup=get_confirmation_keyboard(broadcast_id)
    )


@router.message(F.photo, Command("photo"))
async def broadcast_with_photo(message: Message, bot: Bot):
    """
    Обробка розсилки з фото
    """
    if not admin_manager.can_edit(message.from_user.id):
        await message.answer("❌ Ця команда тільки для адміністраторів!")
        return

    # Отримуємо текст з підпису
    if not message.caption:
        await message.answer("✏️ Додайте підпис до фото, починаючи з /photo")
        return

    text = message.caption.replace('/photo', '').strip()

    if not text:
        await message.answer("✏️ Введіть текст для розсилки після команди /photo")
        return

    photo_file_id = message.photo[-1].file_id

    # Створюємо унікальний ID для цієї розсилки
    broadcast_id = str(uuid.uuid4())

    # Зберігаємо дані розсилки
    pending_broadcasts[broadcast_id] = {
        'type': 'photo',
        'text': text,
        'file_id': photo_file_id,
        'admin_id': message.from_user.id
    }

    # Відправляємо попередній перегляд (без HTML форматування)
    await message.answer_photo(
        photo=photo_file_id,
        caption=f"📨 ПОПЕРЕДНІЙ ПЕРЕГЛЯД РОЗСИЛКИ\n\n"
                f"Тип: Фото\n"
                f"Текст:\n{text}\n\n"
                f"👥 Отримають: {get_subscribed_users_count()} користувачів",
        reply_markup=get_confirmation_keyboard(broadcast_id)
    )


@router.message(F.video, Command("video"))
async def broadcast_with_video(message: Message, bot: Bot):
    """
    Обробка розсилки з відео
    """
    if not admin_manager.can_edit(message.from_user.id):
        await message.answer("❌ Ця команда тільки для адміністраторів!")
        return

    # Отримуємо текст з підпису
    if not message.caption:
        await message.answer("✏️ Додайте підпис до відео, починаючи з /video")
        return

    text = message.caption.replace('/video', '').strip()

    if not text:
        await message.answer("✏️ Введіть текст для розсилки після команди /video")
        return

    video_file_id = message.video.file_id

    # Створюємо унікальний ID для цієї розсилки
    broadcast_id = str(uuid.uuid4())

    # Зберігаємо дані розсилки
    pending_broadcasts[broadcast_id] = {
        'type': 'video',
        'text': text,
        'file_id': video_file_id,
        'admin_id': message.from_user.id
    }

    # Відправляємо попередній перегляд (без HTML форматування)
    await message.answer_video(
        video=video_file_id,
        caption=f"📨 ПОПЕРЕДНІЙ ПЕРЕГЛЯД РОЗСИЛКИ\n\n"
                f"Тип: Відео\n"
                f"Текст:\n{text}\n\n"
                f"👥 Отримають: {get_subscribed_users_count()} користувачів",
        reply_markup=get_confirmation_keyboard(broadcast_id)
    )


@router.callback_query(lambda c: c.data and c.data.startswith(('confirm_broadcast:', 'cancel_broadcast:')))
async def process_broadcast_confirmation(callback: CallbackQuery, bot: Bot):
    """Обробка підтвердження або скасування розсилки"""
    global pending_broadcasts

    # Перевіряємо, чи є користувач адміністратором
    if not admin_manager.is_admin(callback.from_user.id):
        await callback.answer("❌ Тільки адміністратори можуть підтверджувати розсилку!", show_alert=True)
        return

    action, broadcast_id = callback.data.split(':')

    # Перевіряємо чи існує така розсилка
    if broadcast_id not in pending_broadcasts:
        await callback.answer("❌ Розсилка застаріла або не знайдена!", show_alert=True)
        await callback.message.delete()
        return

    broadcast_data = pending_broadcasts[broadcast_id]

    # Перевіряємо, чи той самий адмін створив розсилку
    if broadcast_data['admin_id'] != callback.from_user.id:
        await callback.answer("❌ Тільки автор розсилки може її підтвердити!", show_alert=True)
        return

    if action == 'cancel_broadcast':
        # Скасовуємо розсилку
        del pending_broadcasts[broadcast_id]

        if hasattr(callback.message, 'caption') and callback.message.caption:
            await callback.message.edit_caption(
                caption="❌ Розсилку скасовано!",
                reply_markup=None
            )
        else:
            await callback.message.edit_text(
                text="❌ Розсилку скасовано!",
                reply_markup=None
            )
        await callback.answer("Розсилку скасовано")
        return

    # Підтверджуємо розсилку
    await callback.answer("⏳ Розпочинаю розсилку...")

    # Змінюємо повідомлення
    if broadcast_data['type'] == 'text':
        await callback.message.edit_text(
            text=f"⏳ Розпочинаю розсилку...\n\n"
                 f"👥 Всього користувачів: {get_subscribed_users_count()}",
            reply_markup=None
        )
    else:
        await callback.message.edit_caption(
            caption=f"⏳ Розпочинаю розсилку...\n\n"
                    f"👥 Всього користувачів: {get_subscribed_users_count()}",
            reply_markup=None
        )

    # Виконуємо розсилку відповідно до типу
    if broadcast_data['type'] == 'text':
        results = await send_broadcast_message(bot, broadcast_data['text'])
    elif broadcast_data['type'] == 'photo':
        results = await send_broadcast_message_with_photo(
            bot, broadcast_data['text'], broadcast_data['file_id']
        )
    elif broadcast_data['type'] == 'video':
        results = await send_broadcast_message_with_video(
            bot, broadcast_data['text'], broadcast_data['file_id']
        )
    else:
        results = {'total': 0, 'successful': 0, 'failed': 0, 'blocked': 0}

    # Видаляємо дані розсилки
    if broadcast_id in pending_broadcasts:
        del pending_broadcasts[broadcast_id]

    # Формуємо відповідь з результатами
    success_rate = (results['successful'] / results['total'] * 100) if results['total'] > 0 else 0

    await callback.message.answer(
        f"✅ Розсилку завершено!\n\n"
        f"📊 Результати:\n"
        f"• Загалом: {results['total']} 👥\n"
        f"• Успішно: {results['successful']} ✅\n"
        f"• Помилок: {results['failed']} ❌\n"
        f"• Заблоковано: {results['blocked']} 🚫\n\n"
        f"📈 Успішність: {success_rate:.1f}%",
        reply_markup=get_admin_main_keyboard()
    )


# Функція для ініціалізації при старті бота
def init_broadcast_service():
    """Ініціалізація сервісу розсилок"""
    init_users_file()
    print("✅ Сервіс розсилок ініціалізовано")