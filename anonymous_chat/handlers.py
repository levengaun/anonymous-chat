from telegram import Update
from telegram.ext import ContextTypes


def error_handler(func):
    async def wrapper(*args):
        try:
            await func(*args)
        except Exception as e:
            print("Decor handle:", e)

    return wrapper

@error_handler
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    await context.bot.send_message(chat_id=chat_id, text=update.message.text)

@error_handler
async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    await context.bot.send_sticker(chat_id=chat_id, sticker=update.message.sticker)

@error_handler
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    await context.bot.send_photo(chat_id=chat_id, photo=update.message.photo[0])

@error_handler
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    await context.bot.send_video(chat_id=chat_id, video=update.message.video)

@error_handler
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    await context.bot.send_audio(chat_id=chat_id, audio=update.message.audio)

@error_handler
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    await context.bot.send_voice(chat_id=chat_id, voice=update.message.voice)

@error_handler
async def handle_animation(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    await context.bot.send_animation(chat_id=chat_id, animation=update.message.animation)

@error_handler
async def handle_video_note(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    await context.bot.send_video_note(chat_id=chat_id, video_note=update.message.video_note)

@error_handler
async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int, error_message: str):
    await context.bot.send_message(chat_id=chat_id, text=error_message)

