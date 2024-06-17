import logging

from fastapi import APIRouter, HTTPException, Query
from typing import List

from db_client import db

router = APIRouter(prefix='/vinyl_info')


@router.get('/')
async def get_all_vinyls(genres: List[str] = Query(None),
                         countries: List[str] = Query(None),
                         page: int = Query(1, qt=0),
                         sort: str = Query(None)
                         ):
    # size = 20
    # offset = (page - 1) * size
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
            sort_by['rating'] = -1

    # Формируем запрос
    if sort_by:
        vinyls = list(db.vinyl_info.find(query).sort(list(sort_by.items())))
    else:
        vinyls = list(db.vinyl_info.find(query).sort(list({'imgur_img': -1}.items())))

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


@router.get('/artists')
async def get_all_artists():
    artists = list(db.artists_info.find({}))

    if not artists:
        raise HTTPException(status_code=404, detail="WTF")

    for artist in artists:
        artist["_id"] = str(artist["_id"])

    return artists


@router.get('/artists/{artist_slug}')
async def get_artist_by_slug(artist_slug: str):
    artist = db.artists_info.find_one({"slug": artist_slug})

    if not artist:
        raise HTTPException(status_code=404, detail="Publisher Not Found")

    artist["_id"] = str(artist["_id"])

    return artist


@router.get('/artists/{artist_slug}/all_vinyls')
async def get_all_vinyls_of_artist(artist_slug: str):
    query = {
        "artists": {
            "$elemMatch": {
                "name": {"$regex": ".*", "$options": "i"},
                "slug": artist_slug
            }
        }
    }
    all_vinyls = list(db.vinyl_info.find(query))

    if not all_vinyls:
        raise HTTPException(status_code=404, detail="Vinyls Not Found")

    for game in all_vinyls:
        game["_id"] = str(game["_id"])

    return all_vinyls


@router.get('/search/{name}')
async def get_info_by_name(name: str):
    query = {}
    if name:
        query['name'] = {'$regex': name, '$options': 'i'}

    all_info = list(db.vinyl_info.find(query).limit(4))
    for info in all_info:
        info["_id"] = str(info["_id"])

    return all_info


@router.get('/{vinyl_slug}')
async def get_vinyl_by_slug(vinyl_slug: str):
    vinyl = db.vinyl_info.find_one({"slug": vinyl_slug})

    if not vinyl:
        raise HTTPException(status_code=404, detail="Game Not Found")

    vinyl["_id"] = str(vinyl["_id"])

    return vinyl
