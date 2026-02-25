from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

import keyboards as kb
import services.admin_manager as admin_manager
from models.fsm import EditPromo, EditPrice, EditContacts
from services.json_manager import JSONManager

router = Router()


# ===== РЕДАГУВАННЯ АКЦІЇ =====
@router.message(F.text == "✏️ Редагувати акцію")
async def edit_promotion_button(message: Message):
    if not admin_manager.can_edit(message.from_user.id):
        await message.answer("❌ У вас немає прав!")
        return

    promo_text = JSONManager.get_promotion()
    await message.answer(
        f"📢 *Поточна акція:*\n\n{promo_text}\n\nОберіть дію:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb.edit_promotion_keyboard
    )


@router.callback_query(F.data == "edit_promo_text")
async def edit_promo_text_callback(callback: CallbackQuery, state: FSMContext):
    if not admin_manager.can_edit(callback.from_user.id):
        await callback.answer("❌ У вас немає прав!", show_alert=True)
        return

    await callback.answer()
    current_promo = JSONManager.get_promotion()

    text = (
        "📝 *Редагування акції*\n\n"
        f"*Поточний текст:*\n{current_promo}\n\n"
        "👇 *Введіть новий текст акції:*\n\n"
        "Або натисніть /cancel для скасування"
    )

    await callback.message.edit_text(text, parse_mode=ParseMode.MARKDOWN)
    await state.set_state(EditPromo.waiting_for_text)


@router.message(EditPromo.waiting_for_text)
async def process_promo_text(message: Message, state: FSMContext):
    if message.text.lower() in ["/cancel", "❌ скасувати"]:
        await state.clear()
        await message.answer("❌ Скасовано", reply_markup=kb.admin_panel)
        return

    if JSONManager.update_promotion(message.text):
        await message.answer(
            "✅ *Текст акції успішно оновлено!*",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.answer("❌ Помилка при збереженні")

    await state.clear()
    await message.answer("👑 Адмін-панель", reply_markup=kb.admin_panel)


# ===== РЕДАГУВАННЯ ЦІН =====
@router.message(F.text == "💰 Редагувати ціни")
async def edit_prices_button(message: Message):
    if not admin_manager.can_edit(message.from_user.id):
        await message.answer("❌ У вас немає прав!")
        return

    price_text = JSONManager.get_price()
    await message.answer(
        f"💰 *Поточні ціни:*\n\n{price_text}\n\nОберіть дію:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb.edit_prices_keyboard
    )


@router.callback_query(F.data == "edit_price_text")
async def edit_price_text_callback(callback: CallbackQuery, state: FSMContext):
    if not admin_manager.can_edit(callback.from_user.id):
        await callback.answer("❌ У вас немає прав!", show_alert=True)
        return

    await callback.answer()
    current_price = JSONManager.get_price()

    text = (
        "💰 *Редагування цін*\n\n"
        f"*Поточний текст:*\n{current_price}\n\n"
        "👇 *Введіть новий текст цін:*\n\n"
        "Або натисніть /cancel для скасування"
    )

    await callback.message.edit_text(text, parse_mode=ParseMode.MARKDOWN)
    await state.set_state(EditPrice.waiting_for_text)


@router.message(EditPrice.waiting_for_text)
async def process_price_text(message: Message, state: FSMContext):
    if message.text.lower() in ["/cancel", "❌ скасувати"]:
        await state.clear()
        await message.answer("❌ Скасовано", reply_markup=kb.admin_panel)
        return

    if JSONManager.update_price(message.text):
        await message.answer(
            "✅ *Ціни успішно оновлено!*",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await message.answer("❌ Помилка при збереженні")

    await state.clear()
    await message.answer("👑 Адмін-панель", reply_markup=kb.admin_panel)
