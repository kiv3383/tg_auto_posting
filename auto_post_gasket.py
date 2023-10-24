import logging

import os

from telethon.sync import TelegramClient
from telethon import events

# from auto_post_target_group import admin_target_group_id, target_group
from config_data.config import AllSettings

all_settings = AllSettings()

formatter = logging.Formatter()
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

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
    # file = message.media
    # text = message.message
    # print(message)
    # print('file:', file)
    # print('text:', text)
    if message.grouped_id:
        return
    await client.send_message(gasket_group, message)
    # await bot.send_message(admin_target_group_id, message=text, file=file, buttons=Button.inline('ДА'))


@client.on(events.Album(chats=source_group))
async def album_handler(event):
    files = [f.media for f in event.messages]
    await client.send_message(gasket_group, event.messages[0].message, file=files)
    print('send from source to gasket')
    print('text:', event.messages[0].message)
    print('files:', files)


async def get_message_for_bot(group, ids):
    result = await client.get_messages(group, ids=ids)
    return result


async def send_album_message_to_target_channel(group, text, file, silent):
    await client.send_message(group, message=text, file=file, silent=silent)


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
