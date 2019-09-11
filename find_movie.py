'''
Модуль, в котором будут содержаться классы и функции, относящиеся к поиску и рекомендации фильмов
'''

from tmdbv3api import TMDb, Movie

import config

tmdb = TMDb()
tmdb.api_key = config.tmdb_api_key
tmdb.language = config.tmdb_language


def search_movie(request):
    '''
    Функция поиска фильма (в названиях) по запросу. На вход получает строку запроса,
    на выходе выдает список, содержащий объекты-фильмы в виде словаря {поле-значение}
    :param request:
    :return search:
    '''

    movie = Movie()
    search = movie.search(request)
    #print(len(search))
    #for res in search:
    #    print(res.id)
    #    print(res.title, '['+res.original_title+']')
    #    print(res.entries.items())
    return search


def multi_search(request):
    """
    Функция поиска среди фильмов, сериалов, актеров
    TO DO в tmdbv3api отсутствует функция мультипоиска, поэтому придется подключать еще одну библиотеку
    но реализовывать её буду после бета-запуска бота

    :param request:
    :return:
    """



if __name__ == '__main__':
    q = 'matrix'
    srch = search_movie(q)
    print('length', len(srch))

    for res in srch:
        print(res.title)
        print(res.release_date)
        print(res.poster_path)
        print(res.__dict__)
