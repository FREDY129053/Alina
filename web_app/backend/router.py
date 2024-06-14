from fastapi import APIRouter, HTTPException, Query
from typing import List

from db_client import db

router = APIRouter(prefix='/vinyl_info')


@router.get('/')
async def get_all_vinyls(genres: List[str] = Query(None),
                        countries: List[str] = Query(None),
                        # sort: str = Query(None)
                         ):
    query = {}  # Запрос
    sort_by = {}  # Запрос на сортировку
    # Если передаются параметры, то запоминаем
    if genres:
        query['genres'] = {'$all': genres}
    if countries:
        query['country'] = {'$all': countries}
    # TODO: написать параметры сортировки
    # if sort:
    #     if sort.lower() == 'date':
    #         sort_by['date.year'] = -1
    #     elif sort.lower() == 'rating':
    #         sort_by['score'] = -1
    # Формируем запрос
    vinyls = list(db.vinyl_info.find(query))
    print(f'DB = {query}')

    # if sort_by:
    #     vinyls = vinyls.sort(list(sort_by.items()))

    for vinyl in vinyls:
        vinyl["_id"] = str(vinyl["_id"])

    result = {
        "vinyls": vinyls,
    }

    return result


@router.get('/filters')
async def get_all_filters():
    filters = {}
    genres = list(db.vinyl_info.distinct("genres"))
    countries = list(db.vinyl_info.distinct("country"))
    filters['genres'], filters['countries'] = genres, countries

    return filters
