import re
import time
from slugify import slugify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import discogs_client
from bson.objectid import ObjectId

# all_artists = set()

def get_collection_connection(collection_name):
    try:
        conn = MongoClient()
    except:
        return
    db = conn.vinyl_db
    collection = db[collection_name]

    return collection

def api_parse():
    d = discogs_client.Client('database_app/1.0', user_token='vOARcPUowVOuOyEwajkFQQfiWGWzIJGozEiLCuIv')

    collection = get_collection_connection('vinyl_info')
    vinyls = list(collection.find({}))
    for i in vinyls:
        i['_id'] = str(i['_id'])

    for i, vinyl in enumerate(vinyls):
        print(f'{i} - {vinyl["name"]}')
        results = d.search(vinyl['name'], type='release')

        if results is None or len(results) == 0:
            continue
        else:
            query_filter = {'_id': ObjectId(vinyl['_id'])}
            year = int(results[0].year)
            time.sleep(1.5)
            update_operation = {'$set': {'year': year}}
            result = collection.update_one(query_filter, update_operation)

    # results = d.search('Good Kid, M.A.A.d City', type='release')[0]
    # # results_fil = [i for i in results if i.title.split(' - ')[0] == 'My Chemical Romance']
    # count, n = 0, 1
    # # print(len(results_fil))
    # for i in results:
    #     # print(i)
    #     # print(f'{count}: {i.title} - {i.artists}')
    #     count += 1
    #     if count >= n + 1:
    #         break
    #     # Название
    #     title = i.title.split(" - ")[-1]
    #     print(f'{title} - {i.year}')

        # Страна
        # country = i.country

        # Картинки
        # images = i.images
        # main_photo, other_photos = None, []
        # for img in images:
        #     if img['type'] == 'primary':
        #         main_photo = img['resource_url']
        #     else:
        #         height = re.search(r'h:\d*', img['resource_url']).group(0).split(':')
        #         if int(height[-1]) < 700:
        #             other_photos.append(img['resource_url'])
        #
        # # Трек лист
        # tracklist = i.tracklist
        # db_tracklist = []
        # for j in tracklist:
        #     db_tracklist.append({
        #         "name": j.title,
        #         "duration": j.duration if j.duration != "" else None
        #     })
        #
        # # Жанры
        # genres = i.genres
        #
        # # Рейтинг
        # rating = i.community.rating.data['average']
        #
        # # Исполнители
        # artists = i.artists
        # # print(artists)
        # artists_names = []
        # # print(count)
        # time.sleep(2)
        # for fsd in artists:
        #     info = requests.get(fsd.data['resource_url']).json()
        #     time.sleep(2)
        #     # TODO задержка больше и модифицированный парсинг wiki
        #     if 'message' in list(info.keys()):
        #         print(info)
        #         print(artists)
        #         print('\n')
        #     artist_name = info['name'] if 'name' in list(info.keys()) else fsd.data['name']
        #     artist_profile = info['profile'].split('\n')[0] if 'profile' in list(info.keys()) else None
        #     artist_photo = fsd.data['thumbnail_url'] if fsd.data['thumbnail_url'] != '' else None
        #     artist_url, paragraph = None, None
        #     # print(info)
        #     if 'urls' in list(info.keys()):
        #         for link in info['urls']:
        #             if '.wikipedia.' in link:
        #                 # print(f'{artist_name} - {link}')
        #                 artist_url = link.split(' - ')[-1]
        #
        #     # Парсинг инфы с Вики
        #     if artist_url is not None:
        #         wiki = requests.get(artist_url)
        #         while wiki.status_code != 200:
        #             wiki = requests.get(artist_url)
        #         wiki_page = BeautifulSoup(wiki.text, 'html.parser')
        #
        #         info_paragraphs = wiki_page.find('div', class_='mw-content-ltr mw-parser-output')
        #         paragraphs = info_paragraphs.find_all('p')
        #         paragraph = None
        #         for i in paragraphs:
        #             if i.has_attr('class'):
        #                 continue
        #             else:
        #                 paragraph = i.text
        #                 break
        #         # print(paragraph)
        #
        #     if paragraph is not None:
        #         artist_profile = paragraph
        #     if artist_profile == '' or artist_profile is None:
        #         artist_profile = None
        #
        #     artists_names.append({
        #         "name": artist_name,
        #         "slug": slugify(artist_name)
        #     })
        #     artist = {
        #         "name": artist_name,
        #         "slug": slugify(artist_name),
        #         "photo": artist_photo,
        #         "profile": artist_profile,
        #     }
        #     artists_collection = get_collection_connection('artists_info')
        #
        #     if artists_collection.find_one({'slug': slugify(artist_name)}) is None:
        #         artists_collection.insert_one(artist)
        #     else:
        #         continue
        #     # all_artists.add(artist["name"])
        # print(f'{count} - {title}')
        # vinyl = {
        #     "name": title,
        #     "slug": slugify(title),
        #     "country": country,
        #     "rating": rating,
        #     "photo": main_photo,
        #     "genres": genres,
        #     "all_photos": other_photos,
        #     "artists": artists_names,
        #     "tracklist": db_tracklist
        # }
        # vinyl_collection = get_collection_connection('vinyl_info')
        #
        # if vinyl_collection.find_one({'slug': slugify(title)}) is None:
        #     vinyl_collection.insert_one(vinyl)
        # else:
        #     continue

        # print(artist)
        # print('\n')
        # print(vynil)
        # print('\n')
        # print(len(all_artists))
        # count += 1


def main():
    api_parse()


if __name__ == '__main__':
    main()
