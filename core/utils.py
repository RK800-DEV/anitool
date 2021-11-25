from bs4 import BeautifulSoup
import requests

HEADERS = {
    'authority':'jut.su',
    'method':'POST',
    'path':'/search/',
    'scheme':'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
    'cache-control': 'no-cache',
    'content-length': '43',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://jut.su',
    'pragma': 'no-cache',
    'referer': 'https://jut.su/',
    'sec-ch-ua': '"Microsoft Edge";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
}
DEFAULT_CHECKING_SERVICE = 'https://jut.su/search/'
BLOCKED_MESSAGE_CONTENTS = [
    'К сожалению, в Казахстане контент этой страницы недоступен.',
    'Мы работаем над восстановлением.'
]
AVAILABLE_WEBSITES = [
    'https://gogoanime.vc',
    'https://animevost.am',
    'https://anime.anidub.life/',
]


def SearchAnime(name):
    SearchData = {
        'makeme':'yes',
        'ystext':name.encode('cp1251'),
    }
    client = requests.session()
    SearchRequest = client.post(DEFAULT_CHECKING_SERVICE, data=SearchData, headers=HEADERS)
    print(SearchRequest.url)
    return SearchRequest


def isAvailable(ParsableHTML):
    soup = BeautifulSoup(ParsableHTML, 'html.parser')
    available = soup.find("a", class_="short-btn black video the_hildi")
    if available:
        return True


def isUnavailable(ParsableHTML):
    soup = BeautifulSoup(ParsableHTML, 'html.parser')
    unavailable = soup.find("div", class_="anime_next_announce_msg_text")
    if unavailable:
        return True


def NotFound(ParsableHTML):
    soup = BeautifulSoup(ParsableHTML, 'html.parser')
    unavailable = soup.find("div", class_="anime_next_announce_msg_text")
    available = soup.find("a", class_="short-btn black video the_hildi")

    if not unavailable:
        if not available:
            return True    


def getAnimeName(ParsableHTML):
    soup = BeautifulSoup(ParsableHTML, 'html.parser')
    h1 = soup.find("h1", class_="header_video allanimevideo anime_padding_for_title").get_text()
    if h1.endswith('все серии и сезоны'):
        anime_name = h1[9:len(h1)-19]
    elif h1.endswith('все серии'):
        anime_name = h1[9:len(h1)-10]
    return anime_name


def CheckAvailability(ParsableHTML):
    soup = BeautifulSoup(ParsableHTML, 'html.parser')

    if soup.find("div", class_="anime_next_announce_msg_text"):
        if soup.find("div", class_="anime_next_announce_msg_text").get_text() in BLOCKED_MESSAGE_CONTENTS:
            return 'unavailable'

    elif soup.find("a", class_="short-btn black video the_hildi"):
       return 'available'

    elif soup.find("td", class_="ya-site-form__search-input"):
        return None
