import os

from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()


class AllSettings:
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')
    phone_number = os.getenv('PHONE_NUMBER')
    source_group = os.getenv('SOURCE_GROUP')
    target_group = os.getenv('TARGET_GROUP')
    gasket_group = os.getenv('GASKET_GROUP')
    password = os.getenv('ACC_PASSWORD')
    proxy = {
        'proxy_type': os.getenv('PROXY_TYPE'),
        'addr': os.getenv('ADDR'),
        'port': int(os.getenv('PORT')),
        'username': os.getenv('USER_NAME'),
        'password': os.getenv('PROXY_PASSWORD'),
        'rdns': bool(os.getenv('RDNS'))
    }