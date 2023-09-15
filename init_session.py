import logging
import os
from telethon import TelegramClient
from config_data.config import AllSettings

os.system('taskkill /IM telegram.exe /F')

all_settings = AllSettings()

formatter = logging.Formatter()
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
logging.basicConfig(level=logging.WARNING)

folder_session = 'session/'

api_id = all_settings.api_id
api_hash = all_settings.api_hash
password = all_settings.password
phone_number = all_settings.phone_number
proxy = all_settings.proxy

client = TelegramClient(folder_session + phone_number, api_id, api_hash, proxy=proxy)
client.start(password=password, phone=phone_number)
if client.is_user_authorized():
    logging.info('Login success')

else:
    logging.info('Login fail')

client.disconnect()
