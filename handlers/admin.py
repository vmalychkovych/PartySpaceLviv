import json

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

import keyboards as kb
import services.admin_manager as admin_manager
from models.fsm import EditPromo, EditPrice, EditContacts, AddModerator, ModeratorManagement
from services import broadcast
from services.json_manager import JSONManager

router = Router()

@router.message(F.text == "👑 Адмінка")
async def admin_button(message: Message):
    user_id = message.from_user.id

    if not admin_manager.can_edit(user_id):
        await message.answer(
            "❌ У вас немає прав доступу!",
            reply_markup=kb.get_start_menu(user_id)
        )
        return

    text = "👑 *Адмін-панель*\n\nОберіть дію з меню нижче:"
    await message.answer(
        text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb.admin_panel
    )


# При натисканні на кнопку:
@router.message(F.text == "📨 Розсилка")
async def broadcast_button(message: Message):
    if not admin_manager.can_edit(message.from_user.id):
        await message.answer("❌ У вас немає прав!")
        return

    users_count = broadcast.get_subscribed_users_count()

    await message.answer(
        f"<b>📨 РОЗСИЛКА ПОВІДОМЛЕНЬ</b>\n\n"
        f"<b>👥 Підписано користувачів:</b> <code>{users_count}</code>\n\n"

        f"<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
        f"<b><u>📝 ТИПИ РОЗСИЛОК</u></b>\n"
        f"<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n\n"

        f"<b>📌 Текстова розсилка:</b>\n"
        f"<code>/message Ваш текст</code>\n"
        f"<i>Приклад:</i> <code>/message Сьогодні знижка 20%!</code>\n\n"

        f"<b>📌 Розсилка з фото:</b>\n"
        f"1. <i>Завантажте фото</i>\n"
        f"2. <i>В підписі напишіть:</i> <code>/photo Ваш текст</code>\n\n"

        f"<b>📌 Розсилка з відео:</b>\n"
        f"1. <i>Завантажте відео</i>\n"
        f"2. <i>В підписі напишіть:</i> <code>/video Ваш текст</code>\n\n"

        f"<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
        f"<b><u>🎨 ФОРМАТУВАННЯ ТЕКСТУ</u></b>\n"
        f"<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n\n"

        f"<b>🔹 Жирний текст:</b> <code>&lt;b&gt;текст&lt;/b&gt;</code> → <b>текст</b>\n"
        f"<b>🔹 Курсив:</b> <code>&lt;i&gt;текст&lt;/i&gt;</code> → <i>текст</i>\n"
        f"<b>🔹 Підкреслений:</b> <code>&lt;u&gt;текст&lt;/u&gt;</code> → <u>текст</u>\n"
        f"<b>🔹 Закреслений:</b> <code>&lt;s&gt;текст&lt;/s&gt;</code> → <s>текст</s>\n"
        f"<b>🔹 Моноширинний:</b> <code>&lt;code&gt;текст&lt;/code&gt;</code> → <code>текст</code>\n\n"

        f"<b>✨ КОМБІНАЦІЇ:</b>\n"
        f"• <b><i>Жирний курсив</i></b>: <code>&lt;b&gt;&lt;i&gt;текст&lt;/i&gt;&lt;/b&gt;</code>\n"
        f"• <b><u>Жирний підкреслений</u></b>: <code>&lt;b&gt;&lt;u&gt;текст&lt;/u&gt;&lt;/b&gt;</code>\n"
        f"• <i><u>Курсив підкреслений</u></i>: <code>&lt;i&gt;&lt;u&gt;текст&lt;/u&gt;&lt;/i&gt;</code>\n"
        f"• <b><i><u>Все разом</u></i></b>: <code>&lt;b&gt;&lt;i&gt;&lt;u&gt;текст&lt;/u&gt;&lt;/i&gt;&lt;/b&gt;</code>\n\n"

        f"<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
        f"<b><u>📋 ПРИКЛАДИ ГОТОВИХ РОЗСИЛОК</u></b>\n"
        f"<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n\n"

        f"<b>🔥 ПРИКЛАД 1 - АКЦІЯ:</b>\n"
        f"<code>&lt;b&gt;🔥 ГАРЯЧА ПРОПОЗИЦІЯ!&lt;/b&gt;</code>\n"
        f"<code>&lt;i&gt;Тільки сьогодні&lt;/i&gt; знижка &lt;b&gt;-20%&lt;/b&gt;</code>\n"
        f"<code>&lt;u&gt;Деталі:&lt;/u&gt; всі коктейлі з меню</code>\n\n"

        f"<b>🎉 РЕЗУЛЬТАТ:</b>\n"
        f"<b>🔥 ГАРЯЧА ПРОПОЗИЦІЯ!</b>\n"
        f"<i>Тільки сьогодні</i> знижка <b>-20%</b>\n"
        f"<u>Деталі:</u> всі коктейлі з меню\n\n"

        f"<b>📰 ПРИКЛАД 2 - НОВИНА:</b>\n"
        f"<code>&lt;b&gt;📰 НОВИНИ ЗАКЛАДУ&lt;/b&gt;</code>\n"
        f"<code>&lt;u&gt;Оновлення меню:&lt;/u&gt;</code>\n"
        f"<code>• &lt;i&gt;Нові літні позиції&lt;/i&gt; 🍹</code>\n"
        f"<code>• &lt;b&gt;Авторські десерти&lt;/b&gt;</code>\n\n"

        f"<b>🎉 РЕЗУЛЬТАТ:</b>\n"
        f"<b>📰 НОВИНИ ЗАКЛАДУ</b>\n"
        f"<u>Оновлення меню:</u>\n"
        f"• <i>Нові літні позиції</i> 🍹\n"
        f"• <b>Авторські десерти</b>\n\n"

        f"<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n"
        f"<b><u>⚠️ ВАЖЛИВІ ПРАВИЛА</u></b>\n"
        f"<b>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━</b>\n\n"

        f"<b>✅ МОЖНА:</b>\n"
        f"• Комбінувати теги: <code>&lt;b&gt;&lt;i&gt;текст&lt;/i&gt;&lt;/b&gt;</code>\n"
        f"• Використовувати емодзі поряд з форматуванням\n"
        f"• Робити багаторядкові повідомлення\n\n"

        f"<b>❌ НЕ МОЖНА:</b>\n"
        f"• Залишати теги незакритими: <code>&lt;b&gt;текст</code> <b>(помилка!)</b>\n"
        f"• Вкладати теги хрест-навхрест: <code>&lt;b&gt;текст &lt;i&gt;текст&lt;/b&gt; текст&lt;/i&gt;</code>\n\n"

        f"<b>📌 ШПАРГАЛКА:</b>\n"
        f"<code>&lt;b&gt;текст&lt;/b&gt;</code> → <b>текст</b>\n"
        f"<code>&lt;i&gt;текст&lt;/i&gt;</code> → <i>текст</i>\n"
        f"<code>&lt;u&gt;текст&lt;/u&gt;</code> → <u>текст</u>\n"
        f"<code>&lt;s&gt;текст&lt;/s&gt;</code> → <s>текст</s>\n"
        f"<code>&lt;code&gt;текст&lt;/code&gt;</code> → <code>текст</code>\n\n"


        f"<b>💡 Порада:</b> <i>Скопіюйте приклад та замініть текст на свій!</i>",

        parse_mode="HTML",
        reply_markup=kb.admin_panel
    )


@router.callback_query(F.data == "back_to_admin_panel")
async def back_to_admin_panel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        "👑 *Адмін-панель*",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb.admin_panel
    )


@router.message(F.text == "👥 Керування модераторами")
async def manage_moderators(message: Message):
    if not admin_manager.is_admin(message.from_user.id):
        await message.answer(
            "❌ *Доступ заборонено*\n\n"
            "Цей розділ доступний тільки адміністраторам!",
            parse_mode="Markdown",
            reply_markup=kb.admin_panel
        )
        return

    # Отримуємо дані
    data = admin_manager.load_admins_data()
    moderators = data.get("moderators", [])

    # Формуємо список модераторів з інформацією
    mods_list = ""
    if moderators:
        for i, mod_id in enumerate(moderators, 1):
            # Спробуємо отримати інформацію про користувача
            try:
                with open('data/users.json', 'r', encoding='utf-8') as f:
                    users = json.load(f)
                user_data = users.get(str(mod_id), {})

                if user_data.get('username'):
                    mods_list += f"{i}. @{user_data['username']} (`{mod_id}`)\n"
                elif user_data.get('first_name'):
                    mods_list += f"{i}. {user_data['first_name']} (`{mod_id}`)\n"
                else:
                    mods_list += f"{i}. `{mod_id}`\n"
            except:
                mods_list += f"{i}. `{mod_id}`\n"
    else:
        mods_list = "• *немає модераторів*"

    text = (
        f"👥 *КЕРУВАННЯ МОДЕРАТОРАМИ*\n\n"
        f"👑 *Головний адмін:* `{admin_manager.MAIN_ADMIN_ID}`\n\n"
        f"📋 *Список модераторів:*\n{mods_list}\n\n"
        f"⚙️ *Як користуватися:*\n\n"
        f"➕ *Додати модератора*\n"
        f"   Натисніть кнопку «➕ Додати» та введіть ID\n\n"
        f"➖ *Видалити модератора*\n"
        f"   Натисніть кнопку «➖ Видалити» та введіть ID\n\n"
        f"📋 *Оновити список*\n"
        f"   Натисніть «📋 Список персоналу»\n\n"
        f"🔍 *Як отримати ID користувача:*\n"
        f"1. Користувач має написати боту\n"
        f"2. Використати команду /myid\n"
        f"3. Переслати повідомлення в @userinfobot\n\n"
        f"👇 *Оберіть дію:*"
    )

    await message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=kb.moderator_management_keyboard
    )


@router.callback_query(F.data == "list_staff")
async def list_staff(callback: CallbackQuery):
    await callback.answer()

    data = admin_manager.load_admins_data()
    admins = data.get("admins", [])
    moderators = data.get("moderators", [])

    # Завантажуємо дані користувачів
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
    except:
        users_data = {}

    def get_user_info(user_id):
        """Отримання інформації про користувача"""
        user_str = str(user_id)
        if user_str in users_data:
            user = users_data[user_str]
            info_parts = []

            # Додаємо username якщо є
            if user.get('username'):
                info_parts.append(f"@{user['username']}")

            # Додаємо ім'я якщо є
            name_parts = []
            if user.get('first_name'):
                name_parts.append(user['first_name'])
            if user.get('last_name'):
                name_parts.append(user['last_name'])
            if name_parts:
                info_parts.append(' '.join(name_parts))

            # Додаємо статус активності
            if user.get('subscribed', True):
                info_parts.append("✅ активний")
            else:
                info_parts.append("❌ відписався")

            if info_parts:
                return f" ({', '.join(info_parts)})"
        return ""

    # Форматуємо список адмінів
    admins_list = ""
    for admin_id in admins:
        user_info = get_user_info(admin_id)
        if admin_id == admin_manager.MAIN_ADMIN_ID:
            admins_list += f"• 👑 `{admin_id}`{user_info} (головний)\n"
        else:
            admins_list += f"• 🔐 `{admin_id}`{user_info}\n"

    # Форматуємо список модераторів
    mods_list = ""
    for mod_id in moderators:
        user_info = get_user_info(mod_id)
        mods_list += f"• 🛠 `{mod_id}`{user_info}\n"

    if not mods_list:
        mods_list = "• *немає модераторів*"

    text = (
        f"📋 *ПОВНИЙ СПИСОК ПЕРСОНАЛУ*\n\n"
        f"👑 *Адміністратори:*\n{admins_list}\n\n"
        f"🛠 *Модератори:*\n{mods_list}\n\n"
        f"📊 *Статистика:*\n"
        f"• Всього адмінів: {len(admins)}\n"
        f"• Всього модераторів: {len(moderators)}\n"
        f"• Загалом персоналу: {len(admins) + len(moderators)}"
    )

    await callback.message.edit_text(
        text,
        parse_mode="Markdown",
        reply_markup=kb.moderator_management_keyboard
    )


@router.callback_query(F.data == "add_moderator")
async def add_moderator_start(callback: CallbackQuery, state: FSMContext):
    """Початок додавання модератора"""
    if not admin_manager.is_admin(callback.from_user.id):
        await callback.answer("❌ Тільки адміністратори можуть додавати модераторів!", show_alert=True)
        return

    await callback.answer()

    await callback.message.edit_text(
        "➕ *ДОДАВАННЯ МОДЕРАТОРА*\n\n"
        "Введіть ID користувача, якого хочете додати:\n\n"
        "📝 *ID має бути:*\n"
        "• тільки цифри\n"
        "• без пробілів\n"
        "• наприклад: `123456789`\n\n"
        "Або натисніть /cancel для скасування",
        parse_mode="Markdown"
    )

    await state.set_state(ModeratorManagement.waiting_for_user_id)
    await state.update_data(action_type="add")


@router.callback_query(F.data == "remove_moderator")
async def remove_moderator_start(callback: CallbackQuery, state: FSMContext):
    """Початок видалення модератора"""
    if not admin_manager.is_admin(callback.from_user.id):
        await callback.answer("❌ Тільки адміністратори можуть видаляти модераторів!", show_alert=True)
        return

    await callback.answer()

    # Отримуємо список поточних модераторів
    data = admin_manager.load_admins_data()
    moderators = data.get("moderators", [])

    # Завантажуємо дані користувачів
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
    except:
        users_data = {}

    # Формуємо список модераторів з інформацією
    mods_list = ""
    if moderators:
        for mod_id in moderators:
            user_info = ""
            if str(mod_id) in users_data:
                user = users_data[str(mod_id)]
                if user.get('username'):
                    user_info = f" (@{user['username']})"
                elif user.get('first_name'):
                    user_info = f" ({user['first_name']})"
            mods_list += f"• `{mod_id}`{user_info}\n"
    else:
        mods_list = "• *немає модераторів*\n"

    await callback.message.edit_text(
        f"➖ *ВИДАЛЕННЯ МОДЕРАТОРА*\n\n"
        f"📋 *Поточні модератори:*\n{mods_list}\n\n"
        f"Введіть ID модератора, якого хочете видалити:\n\n"
        f"Або натисніть /cancel для скасування",
        parse_mode="Markdown"
    )

    await state.set_state(ModeratorManagement.waiting_for_user_id)
    await state.update_data(action_type="remove")


@router.message(ModeratorManagement.waiting_for_user_id)
async def process_moderator_id(message: Message, state: FSMContext):
    """Обробка введеного ID для додавання/видалення модератора"""

    # Перевіряємо чи користувач є адміном
    if not admin_manager.is_admin(message.from_user.id):
        await message.answer("❌ У вас немає прав!")
        await state.clear()
        return

    # Перевіряємо скасування
    if message.text.lower() in ["/cancel", "❌ скасувати", "скасувати"]:
        await state.clear()
        await message.answer(
            "❌ *Операцію скасовано*",
            parse_mode="Markdown",
            reply_markup=kb.admin_panel
        )
        return

    # Перевіряємо чи це число
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer(
            "❌ *Помилка!*\n\n"
            "ID має бути числом (тільки цифри).\n"
            "Спробуйте ще раз або натисніть /cancel",
            parse_mode="Markdown"
        )
        return

    # Отримуємо тип дії
    data = await state.get_data()
    action = data.get("action_type")

    # Завантажуємо дані користувачів для інформації
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
    except:
        users_data = {}

    # Отримуємо інформацію про користувача
    user_info = ""
    if str(user_id) in users_data:
        user = users_data[str(user_id)]
        info_parts = []
        if user.get('username'):
            info_parts.append(f"@{user['username']}")
        if user.get('first_name'):
            name = user['first_name']
            if user.get('last_name'):
                name += f" {user['last_name']}"
            info_parts.append(name)
        if info_parts:
            user_info = f"\n📝 *Інформація:* {', '.join(info_parts)}"
    else:
        user_info = "\n⚠️ *Увага:* Користувач не знайдений в базі. Можливо, він ще не писав боту."

    if action == "add":
        # Додавання модератора
        if admin_manager.add_moderator(user_id):
            # Успішне додавання
            await message.answer(
                f"✅ *МОДЕРАТОРА ДОДАНО!*\n\n"
                f"🆔 *ID:* `{user_id}`{user_info}\n\n"
                f"🔍 *Тепер він може:*\n"
                f"• Редагувати акції\n"
                f"• Редагувати ціни\n"
                f"• Редагувати контакти\n"
                f"• Робити розсилки\n"
                f"• Переглядати статистику",
                parse_mode="Markdown"
            )
        else:
            # Помилка додавання
            await message.answer(
                f"❌ *НЕ ВДАЛОСЯ ДОДАТИ МОДЕРАТОРА*\n\n"
                f"🆔 *ID:* `{user_id}`{user_info}\n\n"
                f"📌 *Можливі причини:*\n"
                f"• Користувач вже є модератором\n"
                f"• Користувач є адміністратором\n"
                f"• Помилка при збереженні",
                parse_mode="Markdown"
            )

    elif action == "remove":
        # Видалення модератора
        if admin_manager.remove_moderator(user_id):
            # Успішне видалення
            await message.answer(
                f"✅ *МОДЕРАТОРА ВИДАЛЕНО!*\n\n"
                f"🆔 *ID:* `{user_id}`{user_info}\n\n"
                f"🔍 *Користувач більше не має прав модератора.*",
                parse_mode="Markdown"
            )
        else:
            # Помилка видалення
            await message.answer(
                f"❌ *НЕ ВДАЛОСЯ ВИДАЛИТИ МОДЕРАТОРА*\n\n"
                f"🆔 *ID:* `{user_id}`{user_info}\n\n"
                f"📌 *Можливі причини:*\n"
                f"• Користувач не є модератором\n"
                f"• Помилка при збереженні",
                parse_mode="Markdown"
            )

    # Очищаємо стан
    await state.clear()

    # Показуємо оновлений список персоналу
    await show_updated_staff_list(message)


async def show_updated_staff_list(message: Message):
    """Показує оновлений список персоналу"""
    data = admin_manager.load_admins_data()
    admins = data.get("admins", [])
    moderators = data.get("moderators", [])

    # Завантажуємо дані користувачів
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)
    except:
        users_data = {}

    def get_user_badge(user_id):
        """Отримання бейджика користувача"""
        user_str = str(user_id)
        if user_str in users_data:
            user = users_data[user_str]
            if user.get('username'):
                return f" (@{user['username']})"
            elif user.get('first_name'):
                return f" ({user['first_name']})"
        return ""

    # Форматуємо список адмінів
    admins_list = ""
    for admin_id in admins:
        badge = get_user_badge(admin_id)
        if admin_id == admin_manager.MAIN_ADMIN_ID:
            admins_list += f"• 👑 `{admin_id}`{badge} (головний)\n"
        else:
            admins_list += f"• 🔐 `{admin_id}`{badge}\n"

    # Форматуємо список модераторів
    mods_list = ""
    for mod_id in moderators:
        badge = get_user_badge(mod_id)
        mods_list += f"• 🛠 `{mod_id}`{badge}\n"

    if not mods_list:
        mods_list = "• *немає модераторів*"

    text = (
        f"👥 *КЕРУВАННЯ МОДЕРАТОРАМИ*\n\n"
        f"📋 *Оновлений список:*\n\n"
        f"👑 *Адміністратори:*\n{admins_list}\n"
        f"🛠 *Модератори:*\n{mods_list}\n\n"
        f"📊 *Всього персоналу:* {len(admins) + len(moderators)} осіб\n\n"
        f"👇 *Оберіть дію:*"
    )

    await message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=kb.moderator_management_keyboard
    )


# Обробник для команди /cancel
@router.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext):
    """Скасування поточної операції"""
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("❌ Немає активної операції для скасування")
        return

    await state.clear()
    await message.answer(
        "❌ *Операцію скасовано*",
        parse_mode="Markdown",
        reply_markup=kb.admin_panel
    )