from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

admin_panel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="✏️ Редагувати акцію"), KeyboardButton(text="💰 Редагувати ціни")],
    [KeyboardButton(text="📨 Розсилка"), KeyboardButton(text="📊 Статистика")],
    [KeyboardButton(text="👥 Керування модераторами")],
    [KeyboardButton(text="🔙 Назад в меню")]
], resize_keyboard=True)

edit_promotion_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📝 Змінити текст", callback_data="edit_promo_text")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_admin_panel")]
])

edit_prices_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📝 Змінити текст цін", callback_data="edit_price_text")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_admin_panel")]
])

moderator_management_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="➕ Додати модератора", callback_data="add_moderator")],
    [InlineKeyboardButton(text="➖ Видалити модератора", callback_data="remove_moderator")],
    [InlineKeyboardButton(text="📋 Список персоналу", callback_data="list_staff")],
    [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_admin_panel")]
])