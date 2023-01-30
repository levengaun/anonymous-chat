import asyncio
from dotenv import load_dotenv
import os
from telegram import Bot

from utils import load_json, save_json

async def main():
    load_dotenv()

    bot = Bot(os.getenv("BOT_TOKEN"))
    counter = 0
    user_banned = []
    users = load_json("./src/data/users.json")
    message = """Hello! Thank you for using our bot!"""
    sent = set()
    for value in list(users.values()):
        print(counter)
        if value["id"] in sent:
            print("skip")
            continue

        try:
            chat = await bot.get_chat_member(chat_id=value["id"], user_id=value["id"])
            print(chat)
            counter += 1
        except Exception as e:
            print(value, e)
            user_banned.append(value)
        
        sent.add(value["id"])

    print(counter)
    # save users that banned bot
    save_json(user_banned, "./src/data/banned.json")



if __name__ == "__main__":
    asyncio.run(main())