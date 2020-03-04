import requests
from bs4 import BeautifulSoup
import re

def getAndParseURL(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return(soup)


html_results = getAndParseURL("https://www.okeechobeefest.com/lineup/")
artists = html_results.find_all(href=re.compile("#modal-lineup-artist"))

artist_set = set()
for artist in artists:
    artist_set.add(''.join(artist.findAll(text=True)))

x = sorted(artist_set)
for artist in x:
    print(artist)