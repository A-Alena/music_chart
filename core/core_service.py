import requests
from bs4 import BeautifulSoup
from .models import Musician

URL = 'https://spotifycharts.com/regional'

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def parse_all_chart():
    """ Парсинг spotify charts.

    :return: list of parsing results.
    """
    results = []
    response = requests.get(URL)
    soup = BeautifulSoup(response.text)
    chart_table = soup.find('table', {'class': 'chart-table'}).find('tbody')
    table_rows = chart_table.find_all('tr')
    for tr in table_rows:
        position = tr.find('td', {'class': 'chart-table-position'}).text
        position = int(position)
        track = tr.find('td', {'class': 'chart-table-track'})
        song = track.find('strong').text
        author = track.find('span').text
        author = remove_prefix(author, 'by ')
        results.append({'pos': position, 'song': song, 'auth': author})
    return results

def update_record(auth, song, pos):
    """ Обновить (или создать если отсутствует) запись в БД.
    """
    new_pos = { 'chart_position': pos }
    obj, created = Musician.objects.update_or_create(auth_name = auth, song_name = song, defaults = new_pos)

def get_all_chart():
    """ Получить весь список записей чарта.

    :return: list of all chart.
    """
    response = []
    for record in Musician.objects.all():
        data = {
            'auth': record.auth_name,
            'song': record.song_name,
            'pos': record.chart_position,
        }
        response.append(data)
    return response

def filter_chart(request: dict):
    """ Получить список записей по исполнителю (auth_name)

    :param request: HTTP requests.
    :return:        list with filtered records.
    """
    auth = request.get('auth_name', '')
    results = Musician.objects.filter(auth_name = auth)
    response = []
    for record in results:
        data = {
            'auth': record.auth_name,
            'song': record.song_name,
            'pos': record.chart_position,
        }
        response.append(data)
    return response
