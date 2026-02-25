import json
import os
from typing import Any, Dict, Optional

DATA_DIR = "data"
TEXT_FILE = os.path.join(DATA_DIR, "text.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")


class JSONManager:
    """Клас для роботи з JSON файлами"""

    @staticmethod
    def ensure_data_dir():
        """Створює папку data, якщо її немає"""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    @staticmethod
    def load_text_data() -> Dict[str, Any]:
        """Завантаження текстових даних (акції, ціни)"""
        JSONManager.ensure_data_dir()
        try:
            with open(TEXT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Створюємо дефолтний файл
            default_data = {
                "action": {
                    "text": "🎉 Святковий сет у подарунок до Дня народження..."
                },
                "price": {
                    "text": "💰 Наші ціни:\n\nБудні: 5000 грн..."
                },
                "contacts": {
                    "text": "📍 Адреса:\nм. Львів, вул. Пасічна, 89а..."
                }
            }
            JSONManager.save_text_data(default_data)
            return default_data
        except Exception as e:
            print(f"Помилка завантаження: {e}")
            return {}

    @staticmethod
    def save_text_data(data: Dict[str, Any]) -> bool:
        """Збереження текстових даних"""
        JSONManager.ensure_data_dir()
        try:
            with open(TEXT_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Помилка збереження: {e}")
            return False

    @staticmethod
    def update_promotion(text: str) -> bool:
        """Оновлення тексту акції"""
        data = JSONManager.load_text_data()
        if "action" not in data:
            data["action"] = {}
        data["action"]["text"] = text
        return JSONManager.save_text_data(data)

    @staticmethod
    def update_price(text: str) -> bool:
        """Оновлення тексту цін"""
        data = JSONManager.load_text_data()
        if "price" not in data:
            data["price"] = {}
        data["price"]["text"] = text
        return JSONManager.save_text_data(data)

    @staticmethod
    def update_contacts(text: str) -> bool:
        """Оновлення тексту контактів"""
        data = JSONManager.load_text_data()
        if "contacts" not in data:
            data["contacts"] = {}
        data["contacts"]["text"] = text
        return JSONManager.save_text_data(data)

    @staticmethod
    def get_promotion() -> str:
        """Отримання тексту акції"""
        data = JSONManager.load_text_data()
        return data.get("action", {}).get("text", "Акція не знайдена")

    @staticmethod
    def get_price() -> str:
        """Отримання тексту цін"""
        data = JSONManager.load_text_data()
        return data.get("price", {}).get("text", "Ціни не знайдено")

    @staticmethod
    def get_contacts() -> str:
        """Отримання тексту контактів"""
        data = JSONManager.load_text_data()
        return data.get("contacts", {}).get("text", "Контакти не знайдено")