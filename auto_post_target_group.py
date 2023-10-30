import logging

import os

from telethon.sync import TelegramClient
from telethon import events, Button

from auto_post_gasket import get_message_for_bot, send_album_message_to_target_channel
from config_data.config import AllSettings

all_settings = AllSettings()

formatter = logging.Formatter()
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)

# os.system('taskkill /IM telegram.exe /F')

root_path = os.path.dirname(os.path.abspath(__file__))
folder_session = root_path + '/session/'

api_id = all_settings.api_id
api_hash = all_settings.api_hash
phone_number = all_settings.phone_number
source_group = all_settings.source_group
gasket_group = all_settings.gasket_group
target_group = all_settings.target_group
admin_target_group_id = all_settings.admin_target_group_id
proxy = all_settings.proxy
bot_token = all_settings.bot_token

session_name = folder_session + phone_number + '_bot'
logging.info(session_name)

bot = TelegramClient(
    session_name, api_id, api_hash, use_ipv6=True, proxy=proxy, system_version="4.16.30-vxDen")


@bot.on(events.NewMessage(chats=gasket_group))
async def handler(event):
    message = event.message
    message.post_author = None
    file = message.media
    if message.grouped_id:
        return
    button = Button.inline("Post it", data=message.id)
    await bot.send_message(admin_target_group_id, message.message, file=file, buttons=button)


@bot.on(events.Album(chats=gasket_group))
async def album_resend_handler(event):
    messages_id_list = ' '.join(map(str, [mes.id for mes in event.messages]))
    button = Button.inline("Post it", data=messages_id_list)
    files = event.messages
    text_message = event.messages[0].message
    await bot.send_message(admin_target_group_id, text_message, file=files)
    await bot.send_message(admin_target_group_id, 'Post previous album_message.', buttons=button)


@bot.on(events.CallbackQuery)
async def handler(event):
    """Sends a message to the target channel when the button is pressed.
     Remove the button to prevent resending."""
    message = await event.get_message()
    messages_id_list = list(map(int, event.data.decode('UTF-8').split()))
    messages_from_album = await get_message_for_bot(gasket_group, ids=messages_id_list)
    message_text = ' '.join(map(lambda x: x.message, messages_from_album))
    files = [message.media for message in messages_from_album]
    if not files[0]:
        files = None
    await send_album_message_to_target_channel(target_group, text=message_text,
                                               file=files, silent=True)
    await bot.edit_message(message, buttons=Button.clear(), link_preview=False)


# @bot.on(events.NewMessage(chats=target_group))
# async def target_message_handler(event):
#     message = event.message
#     print('Новое сообщение в target_group: ', message)


if __name__ == "main":
    bot.start(bot_token=bot_token)
    bot.run_until_disconnected()
