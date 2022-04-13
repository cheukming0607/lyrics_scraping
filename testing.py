from bs4 import BeautifulSoup
import requests

def add_domain(urls, domain):
    urls_with_domain = []
    for url in urls:
        urls_with_domain.append(domain+url)
    return urls_with_domain

urls = ['/twy101153x89x1.htm', '/twy109411x32x1.htm', '/twy109411x32x2.htm']
domain = 'https://mojim.com'

print(add_domain(urls, domain))