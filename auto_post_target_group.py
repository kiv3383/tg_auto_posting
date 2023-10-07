import logging

import os

from telethon.sync import TelegramClient
from telethon import events, Button

from config_data.config import AllSettings

all_settings = AllSettings()

formatter = logging.Formatter()
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

# os.system('taskkill /IM telegram.exe /F')

root_path = os.path.dirname(os.path.abspath(__file__))
folder_session = root_path + '/session/'

api_id = all_settings.api_id
api_hash = all_settings.api_hash
phone_number = all_settings.phone_number
source_group = all_settings.source_group
gasket_group = all_settings.gasket_group
target_group = all_settings.target_group
# password = all_settings.password
proxy = all_settings.proxy
bot_token = all_settings.bot_token

session_name = folder_session + phone_number + '_bot'
logging.info(session_name)

bot = TelegramClient(session_name, api_id, api_hash, proxy=proxy).start(bot_token=bot_token)


# client.connect()
# if not client.is_user_authorized():
#     logging.error('Login fail, check account (' + phone_number + '), need to run init_session')
# else:
#     logging.info('Login success')


@bot.on(events.NewMessage(chats=gasket_group))
async def handler(event):
    message = event.message
    # message['reply_markup'] = ReplyInlineMarkup
    print(event.message)
    markup = bot.build_reply_markup(Button.inline("Опубликовать"))
    await bot.send_message(6377827844, message, buttons=markup)
    await bot.send_message(6377827844, 'lkjflkds', buttons=markup)


# bot.start(bot_token=bot_token)
bot.run_until_disconnected()
