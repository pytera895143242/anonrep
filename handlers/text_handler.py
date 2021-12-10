from aiogram import types
from misc import dp,bot
import asyncio
from .sqlit import del_in_queue,reg_session,cheack_another_chat_id,del_session,reg_gender,cheack_session
from .sqlit import find_man,find_woman,find_any

from .commands import markup_stop,markup_find,markup_gender,markup_stop_dialog

@dp.message_handler(content_types=['text','photo','voice','video','video_note'])
async def all_other_messages(message: types.message):
    if message.chat.type == 'private':
        # ЧЕЛОВЕК УКАЗАЛ СВОЙ ПОЛ 👇👇👇
        if message.text == '🚹 Я парень' and cheack_session(message.chat.id) == '1':
            s = reg_gender(chat_id=message.chat.id,first_name= message.from_user.first_name, gender='man')
            if s != '0':
                await bot.send_message(chat_id=message.chat.id, text='Отлично! Кого будем искать?',reply_markup=markup_find())
            else:
                await bot.send_message(chat_id=message.chat.id, text='Вы уже указывали пол! Кого будем искать?',reply_markup=markup_find())

        elif message.text == '🚺 Я девушка' and cheack_session(message.chat.id) == '1':
            s = reg_gender(chat_id=message.chat.id, first_name=message.from_user.first_name, gender='woman')
            if s != '0':
                await bot.send_message(chat_id=message.chat.id, text='Отлично! Кого будем искать?',reply_markup=markup_find())
            else:
                await bot.send_message(chat_id=message.chat.id, text='Вы уже указывали пол! Кого будем искать?',reply_markup=markup_find())
        # ЧЕЛОВЕК УКАЗАЛ СВОЙ ПОЛ 👆👆👆



        # ЧЕЛОВЕК НАЧИНАЕТ ПОИСК СОБЕСЕДНИКА 👇👇👇
        elif message.text == '🔎 ПАРЕНЬ' and cheack_session(message.chat.id) == '1':
            await bot.send_message(chat_id=message.chat.id, text='🔎 Поиск собеседника', reply_markup=markup_stop())
            answer = find_man(chat_id=message.chat.id)

            if len(answer) == 2:
                await bot.send_message(chat_id= answer[0], text= 'Собеседник найден, можете общаться!',reply_markup=markup_stop_dialog())
                await bot.send_message(chat_id=message.chat.id, text='Собеседник найден, можете общаться!',reply_markup=markup_stop_dialog())


        elif message.text == '🔎 ДЕВУШКА' and cheack_session(message.chat.id) == '1':
            await bot.send_message(chat_id=message.chat.id, text='🔎 Поиск собеседника', reply_markup=markup_stop())
            answer = find_woman(chat_id=message.chat.id)
            if len(answer) == 2:
                await bot.send_message(chat_id=answer[0], text='Собеседник найден, можете общаться!',reply_markup=markup_stop_dialog())
                await bot.send_message(chat_id=message.chat.id, text='Собеседник найден, можете общаться!',reply_markup=markup_stop_dialog())


        elif message.text == '🎲 СЛУЧАЙНЫ ПОЛ 🎲' and cheack_session(message.chat.id) == '1':
            await bot.send_message(chat_id=message.chat.id, text='🔎 Поиск собеседника', reply_markup=markup_stop())
            answer = find_any(chat_id=message.chat.id)
            print(answer)
            if len(answer) == 2:
                await bot.send_message(chat_id=answer[0], text='Собеседник найден, можете общаться!',reply_markup=markup_stop_dialog())
                await bot.send_message(chat_id=message.chat.id, text='Собеседник найден, можете общаться!',reply_markup=markup_stop_dialog())


        # ЧЕЛОВЕК НАЧИНАЕТ ПОИСК СОБЕСЕДНИКА 👆👆👆



        elif message.text == '❌ Остановить поиск' and cheack_session(message.chat.id) == '1':
            del_in_queue(chat_id=message.chat.id)
            await bot.send_message(chat_id=message.chat.id, text='Поиск остановлен. Выбери с кем будешь общаться',reply_markup=markup_find())

        elif message.text == '❌ Остановить диалог':
            print('12312')
            another_id = del_session(message.chat.id)
            await bot.send_message(chat_id=message.chat.id,text='Собеседник отключен',reply_markup=markup_find())
            await bot.send_message(chat_id=another_id, text='Ваш собеседник отключился',reply_markup=markup_find())


        else:
            """Проверяем есть ли у человека действующая сессия"""
            an_id = cheack_another_chat_id(message.chat.id)
            if an_id == '1':
                await bot.send_message(text = 'У вас нет активного чата. С кем будем общаться?',chat_id=message.chat.id,reply_markup=markup_find())
            else:
                await bot.copy_message(chat_id=an_id, from_chat_id=message.chat.id,message_id=message.message_id)



