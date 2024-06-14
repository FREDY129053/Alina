import re

import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from slugify import slugify
from pymongo import MongoClient

all_info_links, all_artists_links = [], []
domen = 'https://www.discogs.com'
headers = {
    'User-Agent': UserAgent()['google chrome']
}


def get_collection_connection(collection_name):
    """
        The get_collection_connection function takes a collection name as an argument
        and returns the connection to that
        collection. If there is no connection, it returns None.

        :param collection_name: Specify which collection to connect to
        :return: A connection to the collection
    """
    try:
        conn = MongoClient()
    except:
        return
    db = conn.vinyl_db
    collection = db[collection_name]

    return collection


def get_vinyls_links(count_of_pages, start=1):
    """
        The get_vinyls_links function takes two arguments:
            count_of_pages - the number of pages to be scraped;
            start - the page from which scraping will begin.

        :param count_of_pages: Determine the number of pages to be parsed
        :param start: Start the cycle from a certain page
        :return: A list of links to the pages of all vinyls
    """
    for i in range(start, count_of_pages + 1):
        # Создание параметров для запроса (url и headers)
        url = f'https://www.discogs.com/ru/search/?type=release&sort=hot%2Cdesc&ev=em_tr&page={i}'

        # Отправка запроса на сервер сайта по url с заголовками
        page = requests.get(url, headers=headers)
        while page.status_code != 200:
            page = requests.get(url, headers=headers)

        # Получение HTML кода страницы для дальнейшей работы
        soup = BeautifulSoup(page.text, "html.parser")

        all_names_links = soup.findAll('a', class_='search_result_title')
        for name in all_names_links:
            all_info_links.append(domen + name.get('href'))


def get_vinyl_full_info(link):
    page = requests.get(link, headers=headers)
    while page.status_code != 200:
        page = requests.get(link, headers=headers)

    soup = BeautifulSoup(page.text, "html.parser")

    # Название пластинки и исполнитель(исполнители)
    name_and_artists = soup.find('h1', class_='title_1q3xW').split(' - ')
    artists, name = re.split(r'[ , &]{1,} ', name_and_artists[0]), name_and_artists[1]
    # Получение ссылок на исполнителей
    artists_links = soup.find('span', class_='link_15cpV').findAll('a')
    for artist_link in artists_links:
        all_artists_links.append(domen + artist_link)

    # Получение года выпуска пластинки
    year = int(soup.find('table', class_='table_1fWaB').find('time').text.split(' ')[-2])

    # Получение страны пластинки
    country_arr = re.split(r'[ , &]{1,} ', soup.find('tr', class_='country').find('td').find('span').text)

    # Получение жанров
    genres = [tag.text for tag in soup.find('tr', class_='genres').find('td').findAll('a')]

    # Получение рейтинга пластинки
    rating = float(soup.find('tr', class_='rating').find('td').find('span').text)

    # Получение основной фотографии пластинки
    main_photo = soup.find('div', class_='image_3rzgk bezel_2NSgk').find('img').get('src')

    # Получение всех фотографий пластинок(кроме основной)
    all_photos = [image.get('src') for image in soup.find('ul', class_='thumbnails_20oKg').findAll('img')]

    # Получение трек-листа
    tracklist_table = soup.find('table', class_='tracklist_3QGRS')
    rows = tracklist_table.find('tbody').find_all('tr')
    track_list = []  # Массив для хранения треков пластинки
    for row in rows:
        position = row.find('td', class_='trackPos_2RCje').text
        name_tag = row.find('span', class_='trackTitle_CTKp4')

        # Случай если есть Bonus Track
        if name_tag is None:
            continue

        name = name_tag.text
        # Обработка получения длительности трека, если нет -> None
        try:
            duration = row.find('td', class_='duration_2t4qr').text
        except:
            duration = None

        # Добавляем в массив объект трек
        track_list.append({
            "position": position,
            "name": name,
            "duration": duration
        })

    # Занесение информации о пластинках в БД
    vinyl_collection = get_collection_connection('vinyl_info')

    vinyl = {
        "name": name,
        "slug": slugify(name),
        "country": country_arr,
        "rating": rating,
        "photo": main_photo,
        "genres": genres,
        "all_photos": all_photos,
        "artists": artists,
        "tracklist": track_list,
        "year": year
    }

    if vinyl_collection.find_one({'slug': slugify(name)}) is None:
        vinyl_collection.insert_one(vinyl)


def get_artist_info(artist_link):
    page = requests.get(artist_link, headers=headers)
    while page.status_code != 200:
        page = requests.get(artist_link, headers=headers)

    soup = BeautifulSoup(page.text, "html.parser")

    name = soup.find('h1', class_='title_1q3xW').text

    photo = soup.find('img', class_='image_3rzgk bezel_2NSgk').get('src')

    profile = soup.find('div', class_='profileContainer_2i5F4')
    profile_text = None
    if profile is None or profile.text == '':
        # Находим ссылку на Wikipedia
        links = soup.find('td', class_='profileLinks_6t32F').findAll('a')
        wiki_link = None
        for link in links:
            if 'en.wikipedia.org' in link.get('href'):
                wiki_link = link.get('href')

        if wiki_link is not None:
            wiki = requests.get(wiki_link)
            while wiki.status_code != 200:
                wiki = requests.get(wiki_link)
            wiki_page = BeautifulSoup(wiki.text, 'html.parser')

            info_paragraphs = wiki_page.find('div', class_='mw-content-ltr mw-parser-output')
            paragraphs = info_paragraphs.find_all('p')
            paragraph = None
            for i in paragraphs:
                if i.has_attr('class'):
                    paragraph = i.text
                    break
            profile_text = paragraph

    artist = {
        "name": name,
        "slug": slugify(name),
        "photo": photo,
        "profile": profile_text,
    }
    artists_collection = get_collection_connection('artists_info')

    if artists_collection.find_one({'slug': slugify(name)}) is None:
        artists_collection.insert_one(artist)


if __name__ == '__main__':
    get_vinyls_links(13)

    for vinyl_link in all_info_links:
        get_vinyl_full_info(vinyl_link)

    for artist_info_link in all_artists_links:
        get_artist_info(artist_info_link)