import requests
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config.bot_config import load_config
from langid import classify


class CheckCity(BaseFilter):
    @staticmethod
    def check_city(message: Message) -> bool:
        vk_api_token = load_config().vk_api_token
        city = message.text
        lang = list(classify(message.text))
        url = 'https://api.vk.com/method/database.getCities?v=5.199&access_token={}&q={}&count=1&lang={}'
        res = requests.get(url.format(vk_api_token, city, lang[0])).json()
        return res['response']['count'] and res['response']['items'][0]['title'] == city

    async def __call__(self, message: Message):
        return self.check_city(message)
