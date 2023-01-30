from datetime import datetime
from dotenv import load_dotenv
import logging
import os
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

from keyboards import START_KEYBOARD, END_KEYBOARD
from handlers import handle_text, handle_sticker, handle_voice
from utils import load_json, save_json, load_txt

load_dotenv()

logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter("%(asctime)s.%(msecs)03d %(levelname)s: %(message)s")
handler = logging.FileHandler("logs.txt", "a", encoding="utf-8")
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)

queue = []
chats = {}
users = load_json(os.path.dirname(__file__)+"/data/users.json")
database = load_json(os.path.dirname(__file__)+"/data/database.json")
banned = set([int(s) for s in load_txt(os.path.dirname(__file__)+"/data/banned.txt")])


def extract_username(update: Update):
    user = update.message.from_user
    username = user.username if user.username is not None else user.first_name
    return username


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡️ Choose an action:", reply_markup=START_KEYBOARD)


async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    # FIXME - members without username can't use bot
    if username is None:
        logger.info(update.message.from_user, "user does not set username")
        return

    banned = set([int(s) for s in load_txt(os.path.dirname(__file__)+"/data/banned.txt")])
    chat_id = update.message.chat_id
    if chat_id in banned:
        await update.message.reply_text("⛔️ You have been blocked for suspicious activity.")
        logger.info(username + " banned user try to start")
        return 

    message = update.message
    # check if user not end the last conversation
    if message.chat_id in chats:
        await end_conversation(update, context)

    if message.chat_id in queue:
        return 

    await message.reply_text("Search for an interlocutor...")
    logger.info(username + " searching...")

    users[message.chat_id] = message.from_user

    if len(queue) == 0:
        queue.append(update.message.chat_id)
        return

    user_chat_id = queue.pop()
    chats[user_chat_id] = message.chat_id
    chats[message.chat_id] = user_chat_id
    logger.info(username + " | " + users[user_chat_id].username + " connected")
    try:
        await context.bot.send_message(chat_id=user_chat_id, text="Interlocutor found.", reply_markup=END_KEYBOARD)
        await context.bot.send_message(chat_id=message.chat_id, text="Interlocutor found.", reply_markup=END_KEYBOARD)
    except Exception as e:
        print(e)


async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(extract_username(update) + " end conversation.")
    user_chat_id = update.message.chat_id

    if user_chat_id not in users:
        await update.message.reply_text("I don't understand this command.", reply_markup=START_KEYBOARD)
        return

    second_user = None
    try:
        second_user = chats[user_chat_id]
        del chats[user_chat_id]
        del chats[second_user]
    except KeyError:
        pass

    try:
        if second_user is not None:
            await context.bot.send_message(chat_id=second_user, text="Interlocutor left the conversation.", reply_markup=START_KEYBOARD)
        await context.bot.send_message(chat_id=user_chat_id, text="💬 You have finished the dialogue with your interlocutor.", reply_markup=START_KEYBOARD)

        copy_db = {}
        for k, v in users.items():
            if type(v) is dict:
                copy_db[k] = v
                continue

            copy_db[k] = v.to_dict()

        save_json(copy_db, os.path.dirname(__file__)+"/data/users.json")
        save_json(database, os.path.dirname(__file__)+"/data/database.json")
    except Exception as e:
        print(e)
    

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    
    if chat_id not in chats:
        await update.message.reply_text("I don't understand this command.")
        return

    receiver = chats[chat_id]
    if update.message.text is not None:
        database.append({"time": datetime.now().timestamp(), "from": users[chat_id].id, "to": users[receiver].id, "text": update.message.text})
        logger.info(users[chat_id].username + " | " + users[receiver].username + " | " + update.message.text)
        
        await handle_text(update, context, receiver)

    elif update.message.sticker is not None:
        logger.info(users[chat_id].username + " | " + users[receiver].username + " | sent sticker")
        await handle_sticker(update, context, receiver)

    elif update.message.voice is not None:
        logger.info(users[chat_id].username + " | " + users[receiver].username + " | sent voice")
        await handle_voice(update, context, receiver)



async def under_development(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.message.chat_id, text="This function is under development.")


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("/next") | filters.Regex("🎲 Random interlocutor"), start_conversation))
    app.add_handler(MessageHandler(filters.Regex("/stop") | filters.Regex("End dialogue"), end_conversation))
    app.add_handler(MessageHandler(filters.Regex("🛠 Profile"), under_development))
    app.add_handler(MessageHandler(filters.ALL, handle))
    
    app.run_polling()