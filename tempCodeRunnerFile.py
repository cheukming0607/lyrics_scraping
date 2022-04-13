soup = BeautifulSoup(html_text, 'lxml')
album = soup.find_all('span', class_='m0a')
print(album)