import requests
import time


from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from temp_data import all_links_of_vinyl

all_info_links, all_artists_links = [], []
domen = 'https://www.discogs.com'
headers = {
    'User-Agent': UserAgent()['google chrome']
}



def get_vinyls_links(count_of_pages, start=1):
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
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_JSON;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
        '''
    })
    driver.get(link)
    time.sleep(9999)
    # #challenge-stage > div > label > input[type=checkbox]
    # /html/body/div/div/div[1]/div/label/input
    # captcha = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/label/input'))).click()
    print(driver.page_source)
    html_page = BeautifulSoup(driver.page_source, "html.parser")

    # Получение названия трека и имени артистов
    # TODO: сделать разделение артистов и получение ссылок на каждого
    name_and_artists = html_page.find('h1', class_='title_1q3xW').split(' - ')
    artists, name = name_and_artists[0], name_and_artists[1]
    print(f'{artists} - {name}')
    return 0

    # Получение страницы пластинки(получается)
    # country_tag = soup.select_one(pathes_to_parse["country"])
    # country = country_tag.text if country_tag else None
    #
    # # Получение даты в формате д-м-г
    # release_date_temp = soup.select_one(pathes_to_parse["release_date"]).text.split(' ')
    # release_date = {
    #     "day": release_date_temp[0] if len(release_date_temp) > 0 else None,
    #     "month": release_date_temp[1] if len(release_date_temp) > 1 else None,
    #     "year": release_date_temp[2] if len(release_date_temp) > 2 else None
    # }
    #
    # # Получаем массив всех жанров
    # genres = soup.select_one(pathes_to_parse["genres"]).text.replace(' & ', ', ').split(', ')

    # Парсинг треклиста пластинки из таблицы
    track_list_table = soup.find('table', class_='tracklist_3QGRS')
    rows = track_list_table.find('tbody').find_all('tr')
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


def main():
    # Получение всех ссылок пластинок для парсинга
    # get_vinyls_links(12)
    for i in all_links_of_vinyl[:11]:
        get_vinyl_full_info(i)
        print('\n')

    # get_vinyl_full_info(all_links_of_vinyl[0])


if __name__ == "__main__":
    main()
