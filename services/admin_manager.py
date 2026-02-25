import json
import os

ADMINS_FILE = 'data/admins.json'
# ID головного адміністратора (той, хто має права додавати/видаляти)
MAIN_ADMIN_ID = [554572834, 501040763]  # твій ID

def load_admins_data():
    """Завантаження даних про адмінів та модераторів"""
    if not os.path.exists(ADMINS_FILE):
        # Створюємо файл з головним адміном
        default_data = {
            "admins": [MAIN_ADMIN_ID],
            "moderators": []
        }
        save_admins_data(default_data)
        return default_data

    try:
        with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"admins": [MAIN_ADMIN_ID], "moderators": []}


def save_admins_data(data):
    """Збереження даних про адмінів та модераторів"""
    try:
        with open(ADMINS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False


def is_admin(user_id: int) -> bool:
    """Перевірка чи користувач адмін"""
    data = load_admins_data()
    return user_id in data.get("admins", [])


def is_moderator(user_id: int) -> bool:
    """Перевірка чи користувач модератор"""
    data = load_admins_data()
    return user_id in data.get("moderators", [])


def can_edit(user_id: int) -> bool:
    """Перевірка чи може користувач редагувати контент (адмін або модератор)"""
    return is_admin(user_id) or is_moderator(user_id)


def add_admin(user_id: int) -> bool:
    """Додавання адміна (тільки адмін)"""
    if not is_admin(user_id):  # Перевіряємо, що користувач ще не адмін
        data = load_admins_data()
        if user_id not in data["admins"]:
            data["admins"].append(user_id)
            return save_admins_data(data)
    return False


def remove_admin(user_id: int) -> bool:
    """Видалення адміна (тільки адмін, не можна видалити головного)"""
    if user_id == MAIN_ADMIN_ID:
        return False  # Не можна видалити головного адміна

    data = load_admins_data()
    if user_id in data["admins"]:
        data["admins"].remove(user_id)
        return save_admins_data(data)
    return False


def add_moderator(user_id: int) -> bool:
    """Додавання модератора (тільки адмін)"""
    data = load_admins_data()
    if user_id not in data["moderators"] and user_id not in data["admins"]:
        data["moderators"].append(user_id)
        return save_admins_data(data)
    return False


def remove_moderator(user_id: int) -> bool:
    """Видалення модератора (тільки адмін)"""
    data = load_admins_data()
    if user_id in data["moderators"]:
        data["moderators"].remove(user_id)
        return save_admins_data(data)
    return False


def get_role_name(user_id: int) -> str:
    """Отримання назви ролі користувача"""
    if is_admin(user_id):
        return "🔐 Адмін"
    elif is_moderator(user_id):
        return "🛠 Модератор"
    else:
        return "👤 Користувач"


def format_staff_list():
    """Форматування списку адмінів та модераторів"""
    data = load_admins_data()

    text = "👥 *Список персоналу:*\n\n"

    text += "🔐 *Адміни:*\n"
    if data["admins"]:
        for admin_id in data["admins"]:
            star = "👑 " if admin_id == MAIN_ADMIN_ID else "• "
            text += f"{star}`{admin_id}`\n"
    else:
        text += "• немає\n"

    text += "\n🛠 *Модератори:*\n"
    if data["moderators"]:
        for mod_id in data["moderators"]:
            text += f"• `{mod_id}`\n"
    else:
        text += "• немає\n"

    return text