from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode

import keyboards as kb
import services.admin_manager as admin_manager
import services.broadcast as broadcast
from services.json_manager import JSONManager

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    broadcast.save_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    role = admin_manager.get_role_name(message.from_user.id)

    await message.answer(
        f"👋 Вас вітає бот закладу Party Space Lviv\n"
        f"*Ваша роль:* {role}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb.get_start_menu(message.from_user.id)
    )


@router.message(Command("help"))
async def help_command(message: Message):
    user_id = message.from_user.id
    help_text = """
🆘 *Довідка Party Space Bot*

👋 *Основні команди:*
/start - перезапустити бота
/help - показати це повідомлення

🍽 *Розділи меню:*
• Меню - перегляд нашого меню
• Акції - актуальні пропозиції
• Наші ціни - вартість послуг
• Контакти - адреса, телефони
• Наш сайт - посилання на сайт
    """

    if admin_manager.can_edit(user_id):
        help_text += "\n\n🔐 *Для адмінів:* натисніть 👑 Адмінка"

    await message.answer(help_text, parse_mode=ParseMode.MARKDOWN)


@router.message(F.text == "🍽 Меню")
async def menu(message: Message):
    await message.answer(
        "🍸 Обирайте страви та напої в меню нижче ⬇️",
        reply_markup=kb.submenu_menu
    )


@router.message(F.text == "🔥 Акції")
async def action(message: Message):
    promo_text = JSONManager.get_promotion()
    await message.answer(promo_text, reply_markup=kb.get_start_menu(message.from_user.id))


@router.message(F.text == "💰 Наші ціни")
async def price(message: Message):
    price_text = JSONManager.get_price()
    await message.answer(price_text, reply_markup=kb.get_start_menu(message.from_user.id))


@router.message(F.text == "📞 Контакти")
async def contact(message: Message):
    contacts_text = """
📍 Адреса:
м. Львів, вул. Пасічна, 89а

📞 Контакти:

🎱 Погодинне бронювання (більярд, теніс, PS):
📲 +38067-923-3877

🎉 Оренда всього простору (події на цілий день):
📲 +38067-354-1099

📸 Слідкуй за нами в Instagram:
✨https://www.instagram.com/partyspace_lviv/✨
    """
    await message.answer(contacts_text, reply_markup=kb.get_start_menu(message.from_user.id))


@router.message(F.text == "🌐 Наш сайт")
async def site(message: Message):
    await message.answer(
        "🌐 Більше інформації на нашому сайті:",
        reply_markup=kb.submenu_site
    )


@router.message(F.text == "🔙 Назад в меню")
async def back_to_menu(message: Message):
    await message.answer(
        "👋 Головне меню:",
        reply_markup=kb.get_start_menu(message.from_user.id)
    )



@router.message(Command("myid"))
async def cmd_myid(message: Message):
    # Отримуємо ID користувача та формуємо гарну відповідь
    user_id = message.from_user.id

    response_text = (
        f"👤 **Інформація про профіль**\n\n"
        f"🆔 Ваш Telegram ID: <code>{user_id}</code>\n\n"
        f"<i>Ви можете натиснути на ID, щоб скопіювати його.</i>"
    )

    await message.answer(response_text, parse_mode="HTML")