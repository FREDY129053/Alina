import re
import time
from slugify import slugify
import requests
from bs4 import BeautifulSoup
import discogs_client
from fake_useragent import UserAgent


def api_parse():
    d = discogs_client.Client('database_app/1.0', user_token='vOARcPUowVOuOyEwajkFQQfiWGWzIJGozEiLCuIv')
    results = d.search(type='release')
    count, n = 1, 4
    for i in results:
        if count >= n + 1:
            break

        title = i.title.split(" - ")[-1]

        # Картинки
        images = i.images
        main_photo, other_photos = None, []
        for img in images:
            if img['type'] == 'primary':
                main_photo = img['resource_url']
            else:
                height = re.search(r'h:\d*', img['resource_url']).group(0).split(':')
                if int(height[-1]) < 700:
                    other_photos.append(img['resource_url'])

        # Трек лист
        tracklist = i.tracklist
        db_tracklist = []
        for j in tracklist:
            db_tracklist.append({
                "name": j.title,
                "duration": j.duration if j.duration != "" else None
            })
            # print(f'{j.title} - {j.duration if j.duration != "" else None}')

        # Жанры
        genres = i.genres

        # Рейтинг
        rating = i.community.rating

        # Исполнители
        artists = i.artists
        for fsd in artists:
            info = requests.get(fsd.data['resource_url']).json()
            artist_name = info['name']
            print(slugify(artist_name))
            artist_profile = info['profile'].split('\n')[0]
            artist_photo = fsd.data['thumbnail_url']
            artist_url = None
            for link in info['urls']:
                if '.wikipedia.' in link:
                    artist_url = link

            # Парсинг инфы с Вики
            if artist_url is not None or not artist_url == '':
                wiki = requests.get(artist_url)
                wiki_page = BeautifulSoup(wiki.text, 'html.parser')
                info_paragraphs = wiki_page.find('div', class_='mw-content-ltr mw-parser-output')
                paragraph = info_paragraphs.find_all('p')[1].text
        count += 1


def main():
    api_parse()


if __name__ == '__main__':
    main()
