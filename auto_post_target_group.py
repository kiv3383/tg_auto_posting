import os
import re

from loguru import logger
from telethon.sync import TelegramClient
from telethon import events, Button
from telethon.utils import get_input_media

from auto_post_gasket import get_message_for_bot, send_album_message_to_target_channel
from config_data.config import AllSettings

all_settings = AllSettings()

logger.add('tg_auto_posting.log', enqueue=True)

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

bot = TelegramClient(
    session_name, api_id, api_hash, use_ipv6=True, proxy=proxy, system_version="4.16.30-vxDen")


@logger.catch
@bot.on(events.NewMessage(chats=gasket_group))
async def handler(event):
    message = event.message
    file = message.media
    if message.grouped_id:
        return

    # TODO: сделать функцию и заменить в модулях
    if getattr(file, 'spoiler', None):
        event.media = get_input_media(event.media)
        event.media.spoiler = True

    button = Button.inline("Post it", data=message.id)
    logger.info(f'Новое сообщение в канале-прокладке и в боте: {message}')
    # await bot.send_message(admin_target_group_id, message.message, file=file, buttons=button)
    await bot.send_message(admin_target_group_id, message, buttons=button)


@logger.catch
@bot.on(events.Album(chats=gasket_group))
async def album_resend_handler(event):
    messages = event.messages
    messages_id_list = ' '.join(map(str, [mes.id for mes in messages]))
    button = Button.inline("Post it", data=messages_id_list)
    # files = event.messages
    text_message = messages[0].message
    logger.info(f'Новое сообщение-альбом в канале-прокладке и в боте: {messages}')
    await bot.send_message(admin_target_group_id, text_message, file=messages)
    await bot.send_message(admin_target_group_id, 'Post previous album_message.', buttons=button)


@bot.on(events.CallbackQuery)
@logger.catch
async def handler(event):
    """Sends a message to the target channel when the button is pressed.
     Remove the button to prevent resending."""
    message = await event.get_message()
    messages_id_list = list(map(int, event.data.decode('UTF-8').split()))
    messages_from_album = await get_message_for_bot(gasket_group, ids=messages_id_list)
    # text = ' '.join(map(lambda x: x.message, messages_from_album))
    target_group_link = target_group[0]
    inviting_text = f'<a href={target_group_link}>\n\nПодписывайтесь на канал!</a>'
    text = messages_from_album[0].message + inviting_text
    if '\n' in text:
        message_text = re.sub(r'^.*\n', '', text)
    else:
        message_text = re.sub(r'^.*', '', text)
    files = [message.media for message in messages_from_album]
    if None in files:
        files = None

    # TODO: how send photo with spoiler
    # print(files[0])
    # print(files[0].spoiler)
    # message = event.message
    # file = message.media
    # if files[0].spoiler:
    #     files[0].media = get_input_media(messages_from_album[0])
    #     print(files[0])
    #     files[0].spoiler = True
    # print(files)
    await send_album_message_to_target_channel(target_group, text=message_text,
                                               file=files, silent=True, parse_mode='html')
    logger.info(f'Сообщение переслано в целевую группу: {messages_from_album}')
    await bot.edit_message(message, buttons=Button.clear(), link_preview=False)


# @bot.on(events.NewMessage(chats=target_group))
# async def target_message_handler(event):
#     message = event.message
#     print('Новое сообщение в target_group: ', message)


if __name__ == "main":
    bot.start(bot_token=bot_token)
    bot.run_until_disconnected()
