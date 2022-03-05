import aiogram
from aiogram import types, Dispatcher, Bot, executor
import logging
from  aiogram.contrib.fsm_storage.memory import MemoryStorage
import random
from time import sleep
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from dp import BotDB
from inline import markup
from btn import markupp
import re
from states import sevgi


BotDB = BotDB('accaunt.db')

logging.basicConfig(level=logging.INFO)

bot = Bot(token='5193959004:AAFxhVLkKNZaIkxs4rW1OJIvMppivmTfUlA')
dp = Dispatcher(bot, storage=MemoryStorage())

soni = 0

@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    if (not BotDB.user_exists(message.from_user.id)):
        await state.update_data(soni=soni+1)
        BotDB.add_user(message.from_user.id,message.from_user.username, message.from_user.full_name)

    await message.answer(f"Assalomu aleykum {message.from_user.first_name}!\n\n<b>Ismingizni kiriting:</b>",parse_mode='html')
    await sevgi.ism1.set()


@dp.message_handler()
async def rest(message: types.Message, state: FSMContext):
    if message.text == '🔄Qayta ishga tushurish':
        await message.answer(f"<b>Ismingizni kiriting: </b>",parse_mode='html')
        await sevgi.ism1.set()


@dp.message_handler(state=sevgi.ism1)
async def tekshirish(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(ism1=answer)
    await message.reply(f"<b>{answer} sevgilingizni ismini kiriting: </b>", parse_mode='html')
    await sevgi.ism2.set()

@dp.message_handler(state=sevgi.ism2)
async def tekshirish(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(ism2=answer)
    data = await state.get_data()
    ism1 = data.get('ism1')
    ism2 = data.get('ism2')
    soni = data.get('soni')

    son = random.randint(0,100)
    i = 0
    msg = await bot.send_message(chat_id=message.chat.id, text=f"<i>Hisoblanmoqda....</i>",parse_mode='html')
    sleep(3)
    while i < son:
        await msg.edit_text(f"<i>Sevgi o'lchanmoqda {i}%...</i>", parse_mode='html')
        i += random.randint(1,3)
        sleep(0.07)

    await msg.edit_text(f"<b>Siz sevgilingizni {i}% yaxshi ko'rar ekansiz!!! </b>", parse_mode='html', reply_markup=markup,)
    await message.answer(f"<b>Qayta ishga tushurish uchun bosing 👇👇👇</b>", parse_mode='html', reply_markup=markupp)

    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
