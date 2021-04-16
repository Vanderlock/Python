# coding=utf8
import requests
from bs4 import BeautifulSoup
import smtplib
import yagmail
import time


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
           'accept': '*/*'}
test_html = 'https://text-you.ru/rus_text_pesni/46888-artjom-pivovarov-jelastichno.html'
test_html2 = 'https://text-you.ru/eng_text_pesni/34198-a-broken-silence-walls-collide.html'
counter_txt = 0

def get_content(url):
    while True:
        try:
            response = requests.get(url, headers=HEADERS)
            break
        except:
            print('Проблема при запросе пытайся еще')
    return response.text


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    name_song = soup.find('h1', ).text
    text_song = soup.find('div', attrs={'class': 'fulltext', })
    song = text_song.findChild('pre')
    song = str(song)
    song = song.replace('<br>', '\n')
    song = song.replace('</pre>', '')
    song = song.replace('<pre>', '')
    song = song.replace('<br/>', '\n')
    song = song.replace('<br />', '\n')
    song = song.replace('</br />', '\n')
    song = song.replace('<br /></br />', '\n')
    song = song.replace('"', '')
    song = song.replace('[]', '')
    artist, name_song = name_song.split(' - ')
    first_letter = f'[status publish ]   [comments off]  [category исполнители на "{artist[0]}", {artist}] [title {artist} - {name_song}]'

    # return artist + ' - ' + name_song + '\n' + first_letter + '\n' + song
    content = first_letter + '\n' + song
    return content
def send_message(parsed_text,counted_url):

    mail1 = "w1dfqk5n@gmail.com"
    pass1 = "Pfhe,f228"
    mail2 = "chervyachok.durachok@gmail.com"
    pass2 = "14882281488228"
    send_to = "nohi410yehu@post.wordpress.com"
    counter = counted_url

    try:

        if counter%2==0:
            receiver = "nohi410yehu@post.wordpress.com"
            body = parsed_text
            yag = yagmail.SMTP(mail2, pass2)
            yag.send(
                to=receiver,
                contents=body,

            )
            print('send from mail {}'.format(mail2))

        if counter%2==1:
            receiver = "nohi410yehu@post.wordpress.com"
            body = parsed_text
            yag = yagmail.SMTP(mail1, pass1)
            yag.send(
                to=receiver,
                contents=body,

            )
            print('send from mail {}'.format(mail1))

    except:

        print("failed to send mail")

def main():

    with open(f"song_urls.txt", "r", encoding="utf-8") as file:
        urls = file.readlines()
    for url in urls:
        html = ''
        temp_url = url.replace('\n','')
        while True:
            try:

                html = get_content(temp_url)
                break
            except:
                print('Проблема при получении контента')
            print(html)
        if html != '':
            while True:
                try:
                    content = parse(html)
                    while True:
                        try:
                            send_message(content,urls.index(url)+1)
                            print('{} line sended'.format(urls.index(url) + 1))
                            break
                        except:
                            print('Проблема при отправке сообщения')
                    break
                except:
                    print('Проблема при парсинге')
        print(url)
        time.sleep(31)
if __name__ == '__main__':
    main()
