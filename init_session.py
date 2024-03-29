import logging
# import os
import os.path

from loguru import logger
from telethon.sync import TelegramClient

from config_data.config import AllSettings

# os.system('taskkill /IM telegram.exe /F')

all_settings = AllSettings()

# formatter = logging.Formatter()
# logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)

folder_session = 'session/'
if not os.path.exists(folder_session):
    os.mkdir(folder_session)

api_id = all_settings.api_id
api_hash = all_settings.api_hash
password = all_settings.password
phone_number = all_settings.phone_number
proxy = all_settings.proxy

client = TelegramClient(folder_session + phone_number, api_id, api_hash, use_ipv6=True, proxy=proxy,
                        system_version="4.16.30-vxDens")
# client.start(password=password, phone=phone_number)
client.start(phone=phone_number)
# print(client(GetStateRequest()))
# print(client(LogOutRequest()))
if client.is_user_authorized():
    logger.info('Login success')

else:
    logger.info('Login fail')

client.disconnect()
