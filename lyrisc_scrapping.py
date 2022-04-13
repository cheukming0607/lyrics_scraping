from pprint import pprint
from bs4 import BeautifulSoup

with open ("lyrics.html", 'r') as html_file:
    content = html_file.read()

    soup = BeautifulSoup(content, 'lxml')
    # song_name = soup.find_all('dt', class_='fsZx2')
    # lyrics = soup.find_all('dd', class_='fsZx3')
    # print(song_name[0].text)
    songs = soup.find_all('div', class_='fsZ')
    for song in songs:
        song_name = song.dt.text
        song_lyrics = song.dd.text.split('：')[-1]
        print(f"song name: {song_name}")
        print(f"lyrics: {song_lyrics}")