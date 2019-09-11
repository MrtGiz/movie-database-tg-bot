"""
Модуль, в котором реализована функция multisearch - поиск фильмов, сериалов, актеров
"""

import config
import tmdbsimple as tmdb

tmdb.API_KEY = config.tmdb_api_key
language = config.tmdb_language


def multi_search(request):
    search = tmdb.Search()
    page = 1
    response = search.multi(query=request, page=page, language=language)
    return response


if __name__ == '__main__':
    request_movie = 'matrix'
    request_tv = 'breaking bad'
    request_actor = 'daniel rad'
    movie = multi_search(request_movie)
    tv = multi_search(request_tv)
    actor = multi_search(request_actor)
    print(type(movie))
    print(movie)

    for res in movie['results']:
        print(type(res))
        if 'original_title' in res:
            print('Movie', res['id'], '---', res['original_title'])
        elif 'original_name' in res:
            print('TV', res['id'], '---', res['original_name'])
        elif 'name' in res:
            print('Actor', res['id'], '---', res['name'])

    #print()
    #print('_________________________')
    #print(tv)
    #print('_________________________')
    #print(actor)
    #print('_________________________')
