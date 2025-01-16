from telethon import TelegramClient
from telethon.errors import UsernameNotOccupiedError
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv('api_id')
api_hash = os.getenv('api_hash')
bot_token = os.getenv('bot_token')

if not api_id or not api_hash or not bot_token:
    raise ValueError("Please set the 'api_id', 'api_hash', and 'bot_token' environment variables.")

# creating a new telegram client (session saved as 'anon')
client = TelegramClient('anon', api_id, api_hash).start(bot_token=bot_token)

async def get_user_id(username):
    try:
        # get the user entity by username
        user = await client.get_entity(username)
        print(username)
        print(user.id)

        # return the user's ID
        return user.id
    except UsernameNotOccupiedError:
        print(f"Username '{username}' does not exist.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
