#!/usr/bin/python3
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, InlineQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config, logging

from uuid import uuid4
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.utils.helpers import escape_markdown

import re

from bot_logic import get_results

############################### Bot ############################################

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    """
    Функция вызова приветственного сообщения в ответ на команду /start
    """
    update.message.reply_text(start_menu_message(),
                              reply_markup=start_menu_keyboard())


def search_input(update, context):
    """
    Функция получения поискового запроса и передачи его в модуль взаимодействия с базой данных фильмов
    Отображение всплывающего меню с результатами поиска
    :param update:
    :param context:
    :return:
    """
    query = update.inline_query.query
    match = re.match(r'/search (.*)', query).group(1)
    # print(query, '|', match1.group(1))
    results = get_results(match)

    update.inline_query.answer(results)


def main_menu(update, context):
    """
    Функция вызова главного меню поиска фильмов
    """
    query = update.callback_query
    query.edit_message_text(text=main_menu_message(),
                            reply_markup=main_menu_keyboard())


def search_menu(update, context):
    query = update.callback_query
    query.edit_message_text(text=search_menu_message(),
                            reply_markup=search_menu_keyboard())


def recommendation_menu(update, context):
    query = update.callback_query
    query.edit_message_text(text=recommendation_menu_message(),
                            reply_markup=recommendation_menu_keyboard())


def watch_list_menu(update, context):
    query = update.callback_query
    query.edit_message_text(text=watch_list_message(),
                            reply_markup=watch_list_keyboard())


############################ Keyboards #########################################

def start_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Перейти к меню поиска', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Поиск по запросу', callback_data='search_1')],
                [InlineKeyboardButton('Рекомендации к фильму', callback_data='recommendation_1')],
                [InlineKeyboardButton('Открыть список "к просмотру"', callback_data='list_to_watch')]]
    return InlineKeyboardMarkup(keyboard)


def search_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Начать поиск',   # callback_data='search_1_1', (в данном случае не нужно,
                                                        # т.к. не отправляет никаких заптосов
                                      switch_inline_query_current_chat='/search ')],
                [InlineKeyboardButton('Вернуться в главное меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def recommendation_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Подобрать подобные',
                                      switch_inline_query_current_chat='/recommend ')],
                [InlineKeyboardButton('Вернуться в главное меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def watch_list_keyboard():
    keyboard = [[InlineKeyboardButton('Открыть список', callback_data='open_list')],
                [InlineKeyboardButton('Вернуться в главное меню', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


############################# Messages #########################################

def start_menu_message():
    return 'Привет! Я бот, который поможет тебе найти фильм для просмотра или информацию о нем.'


def main_menu_message():
    return 'Описание того, какие варианты действий может выбрать пользователь:\n' \
           '1. Поиск по запросу\n' \
           '2. Получение рекомендаций к фильму\n' \
           '3. Вывод списка фильмов, отложенных для просмотра'


def search_menu_message():
    return 'Для запуска поиска введите команду /search, а затем название фильма. Или нажмите на кнопку "Начать поиск"' \
           'под этим сообщением.'


def recommendation_menu_message():
    return 'Для получения рекомендаций к фильму введите его название и я подберу несколько подобных фильмов.'


def watch_list_message():
    return 'Это меню списка к просмотру(в разработке)'


############################# Handlers #########################################

def main():
    updater = Updater(token=config.telegram_token,
                      base_url='https://telegg.ru/orig/bot',
                      use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(InlineQueryHandler(search_input, pattern=r'/search'))

    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(search_menu, pattern='search_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(recommendation_menu, pattern='recommendation_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(watch_list_menu, pattern='list_to_watch'))

    updater.start_polling()

################################################################################


if __name__ == '__main__':
    main()
