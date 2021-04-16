import requests
from bs4 import BeautifulSoup
import csv
from openpyxl import load_workbook

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
           'accept': '*/*'}
symbol_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z',
               'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
               'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
               '1', '2', '3', '4', '5', '6', '7', '8', '9']
FILE = 'names.csv'
saved = 2


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    if 'К сожалению, данная страница для Вас не доступна, возможно был изменен ее адрес или она была удалена. Пожалуйста, воспользуйтесь поиском.' not in r.text:
        return r.text
    return None


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('td', attrs={'class': 'artist_list', })
    values = []
    for splited_html in items:
        temp_items = splited_html.find_all('a')
        for k in temp_items:
            values.append({'name': k.text, 'url': 'https://text-you.ru' + k['href']})
    return values



def main():
    with open(FILE, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Имя исполнителя', 'url'])
        for letter in symbol_list:
            for number in range(1, 100000000):
                url = "https://text-you.ru/songs/{0}-{1}.html".format(letter, number)
                try:
                    status_response = get_html(url)
                    print(url)
                    if status_response != None:
                        list_artists = get_content(status_response)

                        for item in list_artists:
                            writer.writerow([item['name'], item['url']])
                    if status_response == None:
                        break
                except:
                    print('Error')
    print('Done')


if __name__ == '__main__':
    main()
