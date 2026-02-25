from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import services.admin_manager as admin_manager


def get_start_menu(user_id: int = None):
    buttons = [
        [KeyboardButton(text="🍽 Меню")],
        [
            KeyboardButton(text="🔥 Акції"),
            KeyboardButton(text="💰 Наші ціни"),
        ],
        [
            KeyboardButton(text="📞 Контакти"),
            KeyboardButton(text="🌐 Наш сайт")
        ]
    ]

    if user_id and admin_manager.can_edit(user_id):
        buttons.append([KeyboardButton(text="👑 Адмінка")])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


submenu_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🍸 Меню бар", url="https://www.party-space.lviv.ua/menu")],
    [InlineKeyboardButton(text="🔥 Меню гриль", url="https://mbnk.biz/9Q8JXwtzqM/I69AO")]
])

submenu_site = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🌐 Перейти на сайт", url="https://www.party-space.lviv.ua")]
])

cancel_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="❌ Скасувати")]
], resize_keyboard=True)