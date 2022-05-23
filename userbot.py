import datetime
import random
import config
from telethon import TelegramClient, events, sync, types
from telethon.sessions import StringSession
import asyncio
import threading

api_id = config.api_id
api_hash = config.api_hash
session = "1ApWapzMBu4-uQaZphgN2Z4PnSbhjHMokKwbAQXgU16AXti385IflHU8Fo7TSwRQ8JO3cQO1pexEMlGqN66OoCitlMhCTHbZxqOEISaulhXCXsYTyCgF0lty7q-35QqoXB-Ce9TNRkd5Pi09JokPkVnoapvuAqdyM5eyJxERTw7uGk8piS2BuT1jHReEvwdsXYTAVm7gz6BZ6uqAgrxicTlUzLFiOSCyIxmxe6ankZtjrp6I5BYr4BH5a2vM-nHTysEqAP7-NEKFta4-QkrV2W-1pO7HgL_76QTp6RAkzFoF-Nn9ejtNQUWPwd3HstzKB9WgaXXz0uW8p5kLNeN-FL_yGYXr8Fww="
chats = ["bicy_chat_eng"]

client = TelegramClient(StringSession(session), api_id, api_hash)


async def check_account(file):
    this_client = TelegramClient(f"sessions/{file}", config.api_id, config.api_hash, proxy=random.choice(config.proxies))
    # try:
    await this_client.connect()
    if not await this_client.is_user_authorized():
        try:
            await this_client.send_code_request(file.split('.')[0])
            return True
        except :
            print("Phone number is banned.")
            await this_client.disconnect()
            return False
    return True

async def posting(message):
    grps = config.GROUPS
    for k,v in grps.items():
        # print(config.GROUPS[k])
        if not v:
            continue
        while True:
            account = random.choice(v)
            if await check_account(account):
                break
            else:
                config.GROUPS[k].remove(account)
        media = None
        if message.media:
            media = message.media
        txt = None
        if message.message:
            txt = message.message

        async with TelegramClient(f"sessions/{account}", config.api_id, config.api_hash,
                                  proxy=random.choice(config.proxies)) as cl:
            try:
                if media:
                    await cl.send_file(k, file=media, caption=txt)
                else:
                    await cl.send_message(k, txt)
            except:
                pass


def between_callback(args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(posting(args))
    loop.close()


@client.on(events.NewMessage(chats=chats))
async def listener(event):
    new = event.message
    msg = new
    print(new)
    _thread = threading.Thread(target=between_callback, args=(new,))
    _thread.start()


with client:
    client.run_until_disconnected()
