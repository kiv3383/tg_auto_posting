import os
# from pprint import pprint

from telethon.sync import TelegramClient
from telethon import events, types, utils
from loguru import logger
from telethon.tl.types import Channel, MessageEntityUrl, MessageEntityTextUrl
from telethon.utils import get_input_media

from config_data.config import AllSettings

logger.add('tg_auto_posting.log', enqueue=True)
all_settings = AllSettings()

# os.system('taskkill /IM telegram.exe /F')

root_path = os.path.dirname(os.path.abspath(__file__))
folder_session = root_path + '/session/'

api_id = all_settings.api_id
api_hash = all_settings.api_hash
phone_number = all_settings.phone_number
source_group = all_settings.source_group
gasket_group = all_settings.gasket_group
target_group = all_settings.target_group
proxy = all_settings.proxy

session_name = folder_session + phone_number

client = TelegramClient(
    session_name, api_id, api_hash, use_ipv6=True, proxy=proxy, system_version="4.16.30-vxDen")

with client:
    source_group_peer_ids = []
    source_group_info = {}
    for elem in source_group:
        try:
            if elem.isdigit():
                peer_id = utils.get_peer_id(types.PeerChannel(int(elem)))
            else:
                peer_id = client.get_peer_id(elem)
            source_group_peer_ids.append(peer_id)

        except ValueError as er:
            logger.info(er)
            continue

    for el in source_group_peer_ids:
        channel: Channel = client.get_entity(el)
        source_group_info[el] = channel.title


@logger.catch
@client.on(events.NewMessage(chats=source_group_info))
async def message_handler(event):
    chat_id = event.chat_id
    message = event.message
    if message.grouped_id:
        return
    # if chat_id not in source_group_ids.values() or message.grouped_id:
    #     return
    if getattr(event.media, 'spoiler', None):
        event.media = get_input_media(event.media)
        event.media.spoiler = True

    # message.message = 'Перерслано\n' + repr(event.original_update.message.text).replace("'", "").replace("\\n", "\r\n")
    # for entity in message:
    #     if isinstance(entity, MessageEntityUrl):
    #         message.entity = target_group

    # results = message.get_entities_text(MessageEntityUrl)
    # print(results)
    # print(message.entities[0])
    channel_name = source_group_info[chat_id]
    message.message = f'Sent from: {channel_name}\n' + message.message
    logger.info(f'Новое сообщение в канале-доноре: {message}')
    await client.send_message(gasket_group, message)


@logger.catch
@client.on(events.Album(chats=source_group_info))
async def album_handler(event):
    chat_id = event.chat_id
    channel_name = source_group_info[chat_id]
    # if chat_id not in source_group_ids.values():
    #     return
    messages = event.messages

    # files = [f.media for f in messages]
    message = f'Sent from: {channel_name}\n' + messages[0].message
    logger.info(f'Новое сообщение-альбом в канале-доноре: {messages}')
    # await client.send_message(gasket_group, message, file=files)
    await client.send_message(gasket_group, message, file=messages)

    # await client.send_message(entity=gasket_group, file=event.messages,
    #                           message=repr(event.original_update.message.text).replace("'", "").replace("\\n", "\r\n"),
    #                           parse_mode="html")


@logger.catch
async def get_message_for_bot(group, ids):
    result = await client.get_messages(group, ids=ids)
    return result


@logger.catch
async def send_album_message_to_target_channel(group: list, text, file, silent):
    for target in group:
        await client.send_message(target, message=text, file=file, silent=silent)


if __name__ == "__main__":
    client.start()
    client.run_until_disconnected()
