from fastapi import APIRouter, HTTPException, Query
from typing import List

from db_client import db

router = APIRouter(prefix='/vinyl_info')


@router.get('/')
async def get_all_vinyls(genres: List[str] = Query(None),
                         countries: List[str] = Query(None),
                         page: int = Query(1, qt = 0),
                         sort: str = Query(None)
                         ):
    size = 20
    offset = (page - 1) * size
    query = {}  # Запрос
    sort_by = {}  # Запрос на сортировку
    # Если передаются параметры, то запоминаем
    if genres:
        query['genres'] = {'$all': genres}
        
    if countries:
        query['country'] = {'$all': countries}

    if sort:
        if sort.lower() == 'name a-z':
            sort_by['name'] = 1
        elif sort.lower() == 'name z-a':
            sort_by['name'] = -1
        elif sort.lower() == 'rating up':
            sort_by['rating'] = 1
        elif sort.lower() == 'rating down':
            sort_by['name'] = -1

    # Формируем запрос
    vinyls = list(db.vinyl_info.find(query).skip(offset).limit(size))


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
