"""
Модуль, содержащий логику работы бота:
функции поиска, рекомендаций, реализация списка фильмов к просмотру
"""

from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import find_movie, re


def get_search_results(query):
    """
    Получаем результаты поиска фильма по названию

    :param query:
    :return:
    """
    results_list = find_movie.search_movie(query)
    return results_list


def generate_iqra_list(movie_list):
    """
    TO DO:
    1) периодически возникают ошибки, в результате которых не выводится список фильмов
    похоже, что дело в том, что у некоторых фильмов нет постера или даты выхода или чего-то еще
    нужно добавить обработку отсутствующих полей, чтобы не обламывать поиск
    -- добавил проверку наличия постера - пока ошибок не возникает
    2) добавить режиссера и список актеров на главных ролях
    3) картинку для отсутствующих постеров нужно загружать из локального хранилища - сейчас подгружается с сайта

    :param movie_list:
    :return:
    """
    results = list()
    for mov in movie_list:
        title = '{0} ({1}) \n[{2}]'.format(mov.title, re.match(r'\d{4}', mov.release_date).group(), mov.original_title)

        # проверка наличия постера у фильма
        if mov.poster_path is None:
            text_message = '{0}\n\n{1}\n' \
                           'http://media1.myfolio.com/users/getrnd/images/mkay4a6gy1.jpg'.format(title, mov.overview)
            thumb_url = 'http://media1.myfolio.com/users/getrnd/images/mkay4a6gy1.jpg'
        else:
            text_message = '{0}\n\n{1}\n' \
                           'https://image.tmdb.org/t/p/w500{2}'.format(title, mov.overview, mov.poster_path)
            thumb_url = 'https://image.tmdb.org/t/p/w500' + mov.poster_path

        iqra = InlineQueryResultArticle(
            id=uuid4(),
            title=title,
            input_message_content=InputTextMessageContent(text_message),
            reply_markup=None,                                             #тут должна быть кнопка со ссылкой на трейлер
            thumb_url=thumb_url
        )
        results.append(iqra)
    return results


def get_results(query):
    movie_list = get_search_results(query)
    results = generate_iqra_list(movie_list)
    return results


if __name__ == '__main__':
    result = get_search_results('lord of the')

    iqra = generate_iqra_list(result)
    print(*iqra, sep='\n')
