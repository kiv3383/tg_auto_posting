import json
import logging
from python_socks.async_.asyncio import Proxy
# import time

# from telethon import sync, TelegramClient, events
# from telethon import TelegramClient, connection
from telethon import TelegramClient

# from utils import *

formatter = logging.Formatter()
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

with open('config.json', 'r') as f:
    config = json.loads(f.read())

logging.basicConfig(level=logging.WARNING)

# accounts = config['accounts']
folder_session = 'session/'

api_id = int(config['api_id'])
api_hash = config['api_hash']
password = config['password']
phone = config['accounts']
proxy = config['proxy']

client = TelegramClient(folder_session + phone, api_id, api_hash, proxy=proxy)
client.start(password=password, phone=phone)
if client.is_user_authorized():
    logging.info('Login success')

else:
    logging.info('Login fail')

client.disconnect()
