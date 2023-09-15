import logging

from dotenv import load_dotenv
import os

from telethon.sync import TelegramClient

from config_data.config import AllSettings

all_settings = AllSettings()

formatter = logging.Formatter()
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

os.system('taskkill /IM telegram.exe /F')

root_path = os.path.dirname(os.path.abspath(__file__))
folder_session = root_path + '/session/'

api_id = all_settings.api_id
api_hash = all_settings.api_hash
phone_number = all_settings.phone_number
source_group = all_settings.source_group
password = all_settings.password
proxy = all_settings.proxy

session_name = folder_session + phone_number
logging.info(session_name)

client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)
client.connect()
if not client.is_user_authorized():
    logging.error('Login fail, check account (' + phone_number + '), need to run init_session')
else:
    logging.info('Login success')
client.disconnect()