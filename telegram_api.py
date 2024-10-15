import requests
import asyncio

from get_username import get_user_id

TELEGRAM_API_URL = "https://api.telegram.org/bot7673679495:AAF9SHASlr26IBmkNWzEdbIXnHqd5g5oQDE/"


async def create_sticker_pack(username, sticker_pack_name, title, sticker_file, emoji):

    user_id = await get_user_id(username)

    url = TELEGRAM_API_URL + "createNewStickerSet"
    payload = {
        'user_id': user_id,
        'name': sticker_pack_name,
        'title': title,
        'sticker': sticker_file,
        'emojis': emoji
    }
    response = requests.post(url, data=payload)
    return response.json()


async def add_sticker_to_pack(username, sticker_set_name, sticker_file, emoji):

    user_id = await get_user_id(username)

    url = TELEGRAM_API_URL + "addStickerToSet"
    payload = {
        'user_id': user_id,
        'name': sticker_pack_name,
        'sticker': sticker_file,
        'emojis': emoji
    }
    response = requests.post(url, data=payload)
    return response.json()
