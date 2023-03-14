from random import randint
from time import sleep
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
import json

with open("root.json", "r") as file:
    root_list = json.load(file)

headers = {'Accept-Language': 'en-US, en;q=0.5'}


movies = []
pagination = 1
for url in root_list["imdbUrls"]["urls"]:
    if pagination <= 1:
        page = req.get(url=url.format(start=pagination),headers=headers).text
        soup = bs(page, 'html.parser')
        divs = soup.find_all(class_="lister-item mode-advanced")
        for div in divs:
            header = div.find(class_='lister-item-header').text.split('\n')
            information = [div.find(class_='certificate').text,
                           div.find(class_='runtime').text,
                           div.find(class_='genre').text.split(',')]
            rating = div.find(class_='inline-block ratings-imdb-rating').text
            metascore = div.find(class_='inline-block ratings-metascore').text
            description = div.find_all(class_='text-muted')[2].text
            movies.append({
                "title": header[2],
                "raking": header[1],
                "year": header[3],
                "age": information[0],
                "runtime": information[1],
                "genre": information[2],
                "rating": rating,
                "metascore": metascore,
                "description":description
            })
        sleep(randint(2,10))
        pagination += 50
with open("movies.json","w") as file:
    json.dump(movies,file,ensure_ascii=False,indent=2)