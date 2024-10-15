from telethon import TelegramClient
from telethon.errors import UsernameNotOccupiedError

api_id = '25650072'
api_hash = '86741897522343d24d542922c6995441'
bot_token = '7673679495:AAF9SHASlr26IBmkNWzEdbIXnHqd5g5oQDE'

# creating a new telegram client (session saved as 'anon')
client = TelegramClient('anon', api_id, api_hash).start(bot_token=bot_token)

async def get_user_id(username):
    try:
        # connect to client
        # await client.start()

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
    finally:
        await client.disconnect()
