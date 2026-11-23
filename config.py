# тут храним настройки бота - токен берем из .env файла, чтобы не хранить в коде

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
