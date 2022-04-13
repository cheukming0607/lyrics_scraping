from bs4 import BeautifulSoup
import multiprocessing
import concurrent.futures
import requests
import csv


POOL_SIZE = multiprocessing.cpu_count() - 1 # leave 1 for main process
header = ['singer', 'song_name']
f = open('song_list.csv', 'w')
writer = csv.writer(f)
writer.writerow(header)


def reach_lyrics_page(url):
    lookup_list = ['你', '我', '他', '愛']
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    song = soup.find('div', class_='fsZ')
    line_list = []
    lyrics = ''
    singer = song.find('dl', class_='fsZx1')
    singer = singer.get_text(strip=True, separator='\n').splitlines()[0]
    song_name = song.dt.text
    song_lyrics = song.dd.get_text(strip=True, separator='\n').splitlines()
    for line in song_lyrics[2:]:
        if line == '※ Mojim.com\u3000魔鏡歌詞網':
            continue
        line_list.append(line)
        line_list.append('\n')
        lyrics = ''.join(line_list)

    for word in lookup_list:
        if word in lyrics:
            return False
    
    return singer, song_name, lyrics

def reach_month_page():
    song_urls = []
    html_text = requests.get('https://mojim.com/twzlist2021-11.htm').text
    soup = BeautifulSoup(html_text, 'lxml')
    album = soup.find_all('span', class_='m0a')
    for song in album:
        song_url = song.find('a')
        song_url = song_url.get('href')
        song_urls.append(song_url)
    print(song_urls)
    print(len(song_urls))
    return song_urls

def add_domain(urls, domain):
    urls_with_domain = []
    for url in urls:
        urls_with_domain.append(domain+url)
    return urls_with_domain

def main():
    singer_list = []
    song_name_list = []
    lyrics_list = []
    data = []
    domain = 'https://mojim.com'
    song_urls = reach_month_page()
    urls_with_domain = add_domain(song_urls, domain)
    counter = 1
    with concurrent.futures.ProcessPoolExecutor(max_workers=POOL_SIZE) as executor:
        future_to_url = {executor.submit(reach_lyrics_page, url): url for url in urls_with_domain}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            print(f"{counter} done")
            counter += 1
            try:
                result = future.result()
                if result == False:
                    continue
                else:
                    data.append(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
    
    for record in data:
        singer_list.append(record[0])
        song_name_list.append(record[1])
        lyrics_list.append(record[2])
        data = [record[0], record[1]]
        writer.writerow(data)
    print(f"Singer: {len(singer_list)}")
    print(f"Song name: {len(song_name_list)}")
    print(f"lyrics:{len(lyrics_list)}")
    f.close
    return 0

if __name__ == '__main__':
    main()