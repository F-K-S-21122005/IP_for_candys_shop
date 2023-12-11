from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from pyairtable import Api

# Initialize FSM storage
memory_storage = MemoryStorage()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Подключение к API
token = "5579137805:AAEQrKtLv1c2C7kShgexMsmBxlrhSEFkHMM"
bot = Bot(token=token)
dp = Dispatcher(bot, storage=memory_storage)
headers = {"Accept-Language": "ru"}
api_airtable = 'keyQUfkbDSpJUEubX'
api = Api(api_airtable)
#costumers = api.all('appgShUNYK5MxG9PV', 'Клиенты')
catalog = api.all('appgShUNYK5MxG9PV', 'Товар')
basket = dict()
temp = 0
telefone = ' '
email = ' '


# Создание кнопок
markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Добро подаловать в каталог Сладкой покупки',)
).add('⬅⬅⬅⬅⬅')

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = ["Информация"]
button2 = ["Я знаю, что заказать"]
keyboard.row(*button1, *button2)

markup_request2 = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('500 - 1000'),
    KeyboardButton('1000 - 1500'),
    KeyboardButton('1500 - 2000'))
markup_request3 = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('Да я хочу посмотреть еще что-нибудь'),
    KeyboardButton('Нет'))

markup_request5 = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('Новогодний калейдоскоп'),
    KeyboardButton('Новогодний утренник')).row(
    KeyboardButton('Новогодная ночь'),
    KeyboardButton('Детский праздник'),
    KeyboardButton('Веселые ребята')).add('⬅⬅⬅⬅⬅')

Content = InlineKeyboardButton('Состав', callback_data ='Content' )
Oder = InlineKeyboardButton('Заказать', callback_data= 'Oder')     
markup_inlinerequest1 = InlineKeyboardMarkup(row_width = 2).row(Content, Oder)

Phone = InlineKeyboardButton('Телефон', callback_data='phone')
Email = InlineKeyboardButton('Почта', callback_data= 'email')
markup_inlinerequest2 = InlineKeyboardMarkup(row_width=2).row(Phone, Email)





class InputUserData(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()


def get_keys(d):
    lst = basket.keys()
    ans = ''
    for i in range(lst):
        ans = f'{lst[i]}\n'
        ans += ans
    return ans


# Кнопка назад
@dp.message_handler(Text(equals='⬅⬅⬅⬅⬅'))
async def back(msg: types.Message):
    reply_text = "back✅"
    await msg.answer(reply_text,
                     reply_markup=markup_request2)

# Реакция на /start
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer("Что вас интересует?👋", reply_markup=keyboard)
    global costumers
    costumers = api.all('appgShUNYK5MxG9PV', 'Клиенты')
    lst = []

    for i in range(len(costumers)):
        lst.append(costumers[i].get('fields').get('Name'))
    if message.chat.username not in lst:
        api.create('appgShUNYK5MxG9PV', 'Клиенты' , {"Name": message.chat.username, "Количество" : '0', "Подарок": '0', "Телефон" : '0',  "Почта": '0' }, typecast=True)
    
    
    
  


    
    
# Реакция на информацию
@dp.message_handler(Text(equals="Информация"))
async def information(message: types.Message):
    await message.reply(f"——————————————————\nПривет👋\nЯ бот,\nкоторый может помочь вам в выборе товара в магазине сладких новогодних подарков магазина Сладкая покупка.\n"
                        f"Я могу удовлетворить любые ваши запросы. \n"
                        f'❗️❗️ОЧЕНЬ ВАЖНАЯ ИНФОРМАЦИЯ \n Проверьте есть ли у вас ник в телеграмме, если нет, то функция "Заказать" вам недоступна, приятоного пользования'
                        f"——————————————————", reply_markup=markup_request2)

@dp.message_handler(Text(equals="Я знаю, что заказать"))
async def information(message: types.Message):
    await message.reply(f'Хорошо, в нашем магазине представленны товары распределенные по ценовым категориям', reply_markup=markup_request2)



@dp.message_handler(Text(equals="500 - 1000"))
async def Cheapest_items(message: types.Message):
    await message.reply(f'Все подарки в ценовом сегменте 500 - 1000', reply_markup= markup_request5)
   
        



# кнопки для выбора
@dp.message_handler(Text(equals ='Да я хочу посмотреть еще что-нибудь')) 
async def select(message: types.Message):
    
    await message.answer('Отлично👍', reply_markup=markup_request5)

@dp.message_handler(Text(equals ='Нет')) 
async def select(message: types.Message):
    
    await bot.send_message(message.chat.id, f'Отлично теперь мне нужны некоторые данные, чтобы наши работники могли связатся с вами (Укажите либо ваш телефон, либо вашу почту)', reply_markup= markup_inlinerequest2)


    
# Какой подарок
@dp.message_handler(Text(equals=['Новогодний калейдоскоп', 'Новогодний утренник', 'Новогодная ночь', 'Веселые ребята', 'Детский праздник']))
async def name_product(message: types.Message):
    for i in range(len(catalog)):
        if str(message.text) in str(catalog[i].get('fields').get('Notes')):
            await bot.send_message(message.chat.id, f'Отлично вам понравился ' f' ' f"{catalog[i].get('fields').get('Notes')}")
            await bot.send_photo(message.chat.id, photo= catalog[i].get('fields').get('Фото')[0].get('url'), reply_markup= markup_inlinerequest1)
            global temp 
            temp = i


# Состав подарка
@dp.callback_query_handler(text = 'Content')
async def content_product(callback:types.CallbackQuery):
    await callback.message.answer(f"{catalog[temp].get('fields').get('Состав')}")
    await callback.answer('')
    


    
#Количество подарков
@dp.callback_query_handler(text = 'Oder')
async def num_product(callback:types.CallbackQuery):
    await callback.message.answer('Укажите необходимое количество')
    basket[f"{catalog[temp].get('fields').get('Notes')}"] = 0 
    print(basket)
    await InputUserData.step_1.set()


@dp.message_handler(state=InputUserData.step_1, content_types=types.ContentTypes.TEXT)
async def questionnaire_state_1_message(message: types.Message, state: FSMContext):
        global costumers
        costumers = api.all('appgShUNYK5MxG9PV', 'Клиенты')
        async with state.proxy() as basket:
            basket[catalog[temp].get('fields').get('Notes')] = message.text.replace('\n',' ') 
            print(basket)
            for i in range(len(costumers)):
                    if message.chat.username == costumers[i]['fields']['Name']:
                             api.update('appgShUNYK5MxG9PV','Клиенты',costumers[i]['id'], {'Количество': str(basket.values())[14:len(str(basket.values())) - 3]})
                             api.update('appgShUNYK5MxG9PV','Клиенты',costumers[i]['id'], {'Подарок': '\n'.join(basket.keys())})

            await state.finish()
            await bot.send_message(message.chat.id, f'Хотели бы вы заказать, что-нибудь еще?', reply_markup= markup_request3)
            #await bot.send_message(message.chat.id, f'Отлично теперь мне нужны некоторые данные, чтобы наши работники могли связатся с вами', reply_markup= markup_inlinerequest2)



# Контакты пользователя   
@dp.callback_query_handler(text = 'phone')
async def phone_costumers(callback:types.CallbackQuery):
    await callback.message.answer('Укажите свой телефон')
    await InputUserData.step_2.set()

@dp.message_handler(state=InputUserData.step_2, content_types=types.ContentType.TEXT) 
async def questionnaire_state_2_message(message: types.Message, state: FSMContext):
    global telefone
    global costumers
    costumers = api.all('appgShUNYK5MxG9PV', 'Клиенты')
    async with state.proxy() as telefone:
        telefone = message.text.replace('\n', ' ')
        for i in range(len(costumers)):
            if message.chat.username == costumers[i]['fields']['Name']:
                api.update('appgShUNYK5MxG9PV','Клиенты',costumers[i]['id'],{'Телефон': str(telefone)})
            await state.finish()
    await bot.send_message(message.chat.id, f'Спасибо,{message.chat.username} , за заказ. Скоро с вами свяжется наш сотрудник.')

@dp.callback_query_handler(text = 'email')
async def phone_costumers(callback:types.CallbackQuery):
    await callback.message.answer('Укажите свою почту')
    await InputUserData.step_3.set()

@dp.message_handler(state=InputUserData.step_3, content_types=types.ContentType.TEXT) 
async def questionnaire_state_3_message(message: types.Message, state: FSMContext):
    global email
    global costumers
    global F
    costumers = api.all('appgShUNYK5MxG9PV', 'Клиенты')
    async with state.proxy() as email:
        email = message.text.replace('\n', ' ')
        for i in range(len(costumers)):
            if message.chat.username == costumers[i]['fields']['Name']:
                api.update('appgShUNYK5MxG9PV','Клиенты',costumers[i]['id'],{'Почта': str(email)})
            await state.finish()
    await bot.send_message(message.chat.id, f'Спасибо, {message.chat.username}, за заказ. Скоро с вами свяжется наш сотрудник.')






     
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)