#!venv/bin/python
import Echange
import logging
import aiogram
import asyncio
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from Echange import ecvhange_race
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from os import getenv
from sys import exit


# Объект бота
bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Здесь хранятся пользовательские данные.
# Т.к. это словарь в памяти, то при перезапуске он очистится
user_data = {}
callback_numbers = CallbackData("fabnum", "action")







def get_keyboard_base(base=None):
    """
    NOT WORK
    :param base:
    :return:
    """
    buttons = [
        types.InlineKeyboardButton(text=i, callback_data=callback_numbers.new(base=i)) for i in Echange.vall(base=
                                                                                                               base)
    ]
    choose = types.InlineKeyboardButton(text=f"choose base as {base}", callback_data=callback_numbers.new(
        base="choose"))
    keyboard = types.InlineKeyboardMarkup(row_width=5)
    keyboard.add(*buttons)
    keyboard.add(choose)
    return keyboard


def get_keyboard_echange():
    """
    Fix Me
    :return:
    """
    buttons = [
        types.InlineKeyboardButton(text=i, callback_data=callback_numbers.new(action=i)) for i in Echange.vall()
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=5)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_fab():
    """
    эта функция создает кнопки.
    :return:
    """
    # Fiiiiiiix MEEEEEEE (вывести в другую функциию, а также сделать так, чтобы не добавлялась база)
    spec = [
        types.InlineKeyboardButton(text="chang ammount", callback_data=callback_numbers.new(action="ammount")),
        types.InlineKeyboardButton(text="change base currency", callback_data=callback_numbers.new(
            action="base_currency")),
        types.InlineKeyboardButton(text="select exchange currency", callback_data=callback_numbers.new(
            action="exchange")),

    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*spec)
    return keyboard








async def update_num_text_fab(message: types.Message, new_value: str = None, cours:str =
None, base_currency="Work", ammount="Work"):
    """
    Работает
    Эта функция принисает значение и вывоюит курс. Необходимо добавить кодичество и базовую валюты.
    :param message:
    :param new_value:
    :param cours:
    :return:
    """

    if new_value == None and cours == None:
        with suppress(MessageNotModified):
            await message.edit_text(f"You choose: {new_value} \n amount - {ammount} \n from {base_currency} to {new_value} equals - "
                                    f"{cours} ",
                                    reply_markup=get_keyboard_echange())
    else:
        with suppress(MessageNotModified):
            await message.edit_text(f"You choose: {new_value} \n {cours}", reply_markup=get_keyboard_echange())


# async def update_base(message: types.Message, base_currency):
#     with suppress(MessageNotModified):
#         await message.edit_text(f"Choose base for exchange: {base_currency}",reply_markup=get_keyboard_base(base_currency))








async def cmd_exchange(call: types.CallbackQuery):
    """
    Work in progress
    Стартовая программа. вызывает кнопки
    :param message:
    :return:
    """
    user_data[call.from_user.id] = 0
    await call.answer("select the currency to which you want to change the dollar \n ammount = 1 \n base currency "
                         "- USD", reply_markup=get_keyboard_echange())










# @dp.callback_query_handler(callback_numbers.filter(base=Echange.vall()))
# # async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict, base_currency, ammount):
# async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict):
#
#     base = callback_data["base"]
#
#     user_data[call.from_user.id] = base
#     loop = asyncio.get_event_loop()
#     # function_message = await loop.run_in_executor(None, ecvhange_race, action, base_currency, ammount)
#     function_message = await loop.run_in_executor(None, vall, None, base)
#     await update_base(call.message, function_message)
#     await call.answer()





@dp.callback_query_handler(callback_numbers.filter(action=Echange.vall()))
# async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict, base_currency, ammount):
async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict):
    """
    WORK
    Проверяет какую кнопки конвертации выбрали
    Необходимо улучшить, чтобы также получала значение base currency
    :param call:
    :param callback_data:
    :return:
    """
    action = callback_data["action"]

    user_data[call.from_user.id] = action
    loop = asyncio.get_event_loop()
    # function_message = await loop.run_in_executor(None, ecvhange_race, action, base_currency, ammount)
    function_message = await loop.run_in_executor(None, ecvhange_race, action)
    await update_num_text_fab(call.message, Echange.vall(action), function_message)
    await call.answer()




@dp.callback_query_handler(callback_numbers.filter(action=["ammount", "base_currency", "exchange"]))
async def callbacks_num_finish_fab(call: types.CallbackQuery, callback_data: dict):
    """
    NOT WORK
    Задача - проверять какую кнопку выбрали и выполнить необходимые дейстаия.
    не работает из-за функции - amount()
    :param call:
    :param callback_data:
    :return:
    """
    user_value = user_data.get(call.from_user.id, 0)
    action = callback_data["action"]
    if action == "ammount":                                                                  #FIX ME
        user_data[call.from_user.id] = 0
        await amount()
        await call.answer()
    elif action == "base_currency":
        # await update_base(call.message)
        await call.answer()
    elif action == "exchange":
        await update_num_text_fab(call.message)
        await call.answer()
    await call.answer()




@dp.callback_query_handler(callback_numbers.filter(action=["finish"]))
async def callbacks_num_finish_fab(call: types.CallbackQuery):
    """
    WORK
    Выводит итоговое значение
    необходимо дополнить текст
    :param call:
    :return:
    """
    user_value = user_data.get(call.from_user.id, 0)
    await call.message.edit_text(f"Итого: {user_value}")
    await call.answer()

# @dp.callback_query_handler(callback_numbers.filter(base=["choose"]))
# async def callbacks_num_finish_fab(call: types.CallbackQuery):
#
#     await update_num_text_fab(call.message)
#     await call.answer()











@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    """
    WORK
    Запускает стартовое меню.
    :param message:
    :return:
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = ["Exсhange", "grahic"]
    keyboard.add(*button)
    await message.answer("vot you want", reply_markup=keyboard)





@dp.message_handler(Text(equals="Exсhange"))
async def cmd_option(message: types.Message):
    """
    WORK
    Стартовая программа. вызывает кнопки
    :param message:
    :return:
    """
    user_data[message.from_user.id] = 0
    await message.answer("select the currency to which you want to change the dollar \n ammount = 1 \n base currency "
                         "- USD", reply_markup=get_keyboard_fab())

@dp.message_handler(Text(equals ="grahic"))
async def exchange(message: types.Message):
    """
    FIX ME
    Задача, выводить график курса валют
    также надо доваыить кикие валюты выводить
    нет функции отправки файлов.
    :param message:
    :return:
    """
    loop = asyncio.get_event_loop()
    function_message = await loop.run_in_executor(None, ecvhange_race, "RUB")
    await message.answer(function_message)





if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
