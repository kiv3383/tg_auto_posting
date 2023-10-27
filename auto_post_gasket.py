import logging

import os

from telethon.sync import TelegramClient
from telethon import events

from config_data.config import AllSettings

all_settings = AllSettings()

formatter = logging.Formatter()
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)
logging.basicConfig(level=logging.WARNING)

# os.system('taskkill /IM telegram.exe /F')

root_path = os.path.dirname(os.path.abspath(__file__))
folder_session = root_path + '/session/'

api_id = all_settings.api_id
api_hash = all_settings.api_hash
phone_number = all_settings.phone_number
source_group = all_settings.source_group
gasket_group = all_settings.gasket_group
proxy = all_settings.proxy

session_name = folder_session + phone_number
logging.info(session_name)

client = TelegramClient(
    session_name, api_id, api_hash, use_ipv6=True, proxy=proxy, system_version="4.16.30-vxDen")


@client.on(events.NewMessage(chats=source_group))
async def message_handler(event):
    message = event.message
    if message.grouped_id:
        return
    await client.send_message(gasket_group, message)


@client.on(events.Album(chats=source_group))
async def album_handler(event):
    files = [f.media for f in event.messages]
    await client.send_message(gasket_group, event.messages[0].message, file=files)


async def get_message_for_bot(group, ids):
    result = await client.get_messages(group, ids=ids)
    return result


async def send_album_message_to_target_channel(group: list, text, file, silent):
    for target in group:
        await client.send_message(target, message=text, file=file, silent=silent)


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
