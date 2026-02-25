from aiogram.fsm.state import State, StatesGroup

class EditPromo(StatesGroup):
    waiting_for_text = State()

class EditPrice(StatesGroup):
    waiting_for_text = State()

class EditContacts(StatesGroup):
    waiting_for_text = State()

class AddModerator(StatesGroup):
    waiting_for_id = State()

class Broadcast(StatesGroup):
    waiting_for_text = State()
    waiting_for_media = State()

class ModeratorManagement(StatesGroup):
   waiting_for_user_id = State()
   action_type = State()  # 'add' або 'remove'