from telegram import ReplyKeyboardMarkup, KeyboardButton


START_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("🎲 Random interlocutor")],
    [KeyboardButton("🛠 Profile")]
], resize_keyboard=True)


END_KEYBOARD = ReplyKeyboardMarkup([
    [KeyboardButton("End dialogue")],
    [KeyboardButton("🛠 Profile")]
], resize_keyboard=True)