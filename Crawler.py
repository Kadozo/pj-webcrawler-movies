import json
from random import randint
import requests as req
from bs4 import BeautifulSoup as bs
from time import sleep

class Crawler():
    def __init__(self, offset, urlTypes = "imdbUrls", limit = 1, name_save_file = "movies.json") -> None:
        self.root_list = {}
        self.offset = offset
        self.movies = []
        self.headers = {'Accept-Language': 'en-US, en;q=0.5'}
        self.urlTypes = urlTypes
        self.limit = limit
        self.name_save_file = name_save_file
    
    def run(self) -> None:
        print("Reading root urls...")
        self.get_root_list("root.json")
        print("Initializing data catch...")
        self.get_data()
        print("Saving data in json...")
        self.save_data()

    def get_root_list(self, name_file) -> None:
        with open(name_file, "r") as file:
            self.root_list = json.load(file)
    
    def format(self, value, type):
        if value != None:
            match type:
                case "ranking":
                    return value.replace(".", "")
                case "year":
                    return value.replace("(", "").replace(")", "")
                case "rating":
                    return value.replace("\n", "")
                case "description":
                    return value.replace("\n", "")
                case "metascore":
                    return value.replace("\n", "").replace(" ", "").replace("Metascore", "")
                case "genre":
                    genre = []
                    for v in value:
                        genre.append(v.replace("\n", "").replace(" ", ""))
                    return genre
        return value
    
    def check_null(self, div, isArray = False, pos = None):
        if div == None:
            return None
        if isArray:
            return div[pos].text
        else:
            return div.text

    def get_data(self) -> None:
        pagination = 1
        for url in self.root_list[self.urlTypes]["urls"]:
            while pagination <= self.limit:
                print(f"In pagination {pagination} to {pagination + self.offset}.")
                page = req.get(url=url.replace(":start", str(pagination)),headers=self.headers).text
                soup = bs(page, "html.parser")
                divs = soup.find_all(class_="lister-item mode-advanced")
                for div in divs:
                    header = self.check_null(div.find(class_='lister-item-header'))
                    title = None
                    ranking = None
                    year = None
                    if header != None:
                        header = header.split('\n')
                        ranking = header[1]
                        title = header[2]
                        year = header[3]

                    
                    age = self.check_null(div.find(class_='certificate'))
                    runtime = self.check_null(div.find(class_='runtime'))
                    genre = self.check_null(div.find(class_='genre'))
                    if genre != None:
                        genre = genre.split(",")
                    rating = self.check_null(div.find(class_='inline-block ratings-imdb-rating'))
                    metascore = self.check_null(div.find(class_='inline-block ratings-metascore'))
                    description = self.check_null(div.find_all(class_='text-muted'), isArray=True, pos=2)
                    
                    self.movies.append({
                        "title": title,
                        "ranking": self.format(ranking, type="ranking"),
                        "year": self.format(year, type="year"),
                        "age": age,
                        "runtime": runtime,
                        "genre": self.format(genre, type="genre"),
                        "rating": self.format(rating, type="rating"),
                        "metascore": self.format(metascore, type="metascore"),
                        "description":self.format(description, type="description")
                    })
                sleep(randint(2,10))
                pagination += self.offset
    
    def save_data(self) -> None:
        with open(self.name_save_file,"w") as file:
            json.dump(self.movies,file,ensure_ascii=False,indent=2)