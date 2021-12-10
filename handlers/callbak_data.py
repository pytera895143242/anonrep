from aiogram import types
from misc import dp, bot

import asyncio


@dp.callback_query_handler(text = 'qwerty')  # Нажал кнопку Начать смотреть
async def call_one(call: types.callback_query):
    pass
