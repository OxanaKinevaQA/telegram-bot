# импортируем библиотеки
from bs4 import BeautifulSoup
import requests
from telebot import TeleBot, types
import re
from lxml import html


bot = TeleBot(token='5694633810:AAGFh7ipIegg9J5RSCmO3OeqrUIcP2OFIMY', parse_mode='html') # создание бота

# Адрес запроса последней версии Android
page = requests.get('https://ru.wikipedia.org/wiki/%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F_%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D0%B9_Android')
# Parsing the page
tree = html.fromstring(page.content)
# Получение элемента через XPath
h1 = tree.xpath('//*[@id="mw-content-text"]/div[1]/p[4]/a[1]/text()')
print (h1)


# Адрес запроса последней версии IOS
page1 = requests.get('https://support.apple.com/ru-ru/HT201222#:~:text=%D0%90%D0%BA%D1%82%D1%83%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F%20%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%8F%20iOS%20%D0%B8%20iPadOS%20%E2%80%94%2016.2.')
# Parsing the page
tree1 = html.fromstring(page1.content)
# Получение элемента через XPath
h2 = tree1.xpath('//*[@id="sections"]/div[3]/div/ul/li[1]/text()')
y = str(h2[0]).replace('Узнайте, как','')
print(y)



# объект клавиаутры
main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="Android"), types.KeyboardButton(text="IOS")
)

# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_message_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    # не забываем прикрепить объект клавиатуры к сообщению
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет, приятный человек!\nС помощью меня ты можешь узнать последние версии операционных систем. "\
        "Выбери, информацию о какой системе тебе прислать 👇🏻",
        reply_markup=main_menu_reply_markup
    )

# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    # выводим информацию о последней версии ОС
    # или отправляем ошибку
    payload_len = 0
    if message.text == "Android":
        bot.send_message(
        chat_id=message.chat.id,
        text=h1,
        reply_markup=main_menu_reply_markup
    )
    elif message.text == "IOS":
        bot.send_message(
        chat_id=message.chat.id,
        text=y,
        reply_markup=main_menu_reply_markup
    )
    else:
        bot.send_message(chat_id=message.chat.id, text="Не понимаю тебя :(")
        return

# запускаем нашего бота
bot.infinity_polling()