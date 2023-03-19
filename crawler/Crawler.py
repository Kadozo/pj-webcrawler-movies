import json
from random import randint
import requests as req
from bs4 import BeautifulSoup as bs
from time import sleep
from colorama import Fore

class Crawler():
    def __init__(self, offset, site = "imdb", limit = 1) -> None:
        self.offset = offset
        self.headers = {'Accept-Language': 'en-US, en;q=0.5'}
        self.site = site
        self.limit = limit
    
    def run(self, file_name) -> None:
        print(Fore.GREEN + "INFO:   " + Fore.WHITE + f"[reading file] - reading root file {file_name}")
        root_list = self.get_root_list(file_name)
        self.get_data(root_list)

    def get_root_list(self, file_name: str) -> dict:
        with open(file_name, "r") as file:
            list = json.load(file)
        return list
    
    def format(self, value: str, type: str) -> str:
        if value != None:
            match type:
                case "ranking":
                    return value.replace(".", "")
                case "start_year":
                    return value.replace("(", "").replace(")", "").split("–")[0]
                case "end_year":
                    value = value.replace("(", "").replace(")", "").replace(" ", "").split("–")
                    return value[1] if len(value) > 1 else None
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
    
    def check_null(self, div, isArray: bool = False, pos: int = None):
        if div == None:
            return None
        if isArray:
            return div[pos].text
        else:
            return div.text

    def get_data(self, root_list: dict) -> None:
        for url in root_list[self.site]["urls"]:
            data = []
            pagination = 1
            print(Fore.GREEN + "INFO:   " + Fore.WHITE + f"[getting data] - getting data in website: " + Fore.YELLOW + url['url'])
            while pagination <= self.limit:
                print(Fore.GREEN + "INFO:       " + Fore.WHITE + f"[start pagination] - in pagination {pagination} to {pagination + self.offset}.")
                page = req.get(url=url["url"].replace(":start", str(pagination)),headers=self.headers).text
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
                    
                    data.append({
                        "title": title,
                        "ranking": self.format(ranking, type="ranking"),
                        "start_year": self.format(year, type="start_year"),
                        "end_year": self.format(year, type="end_year"),
                        "age": age,
                        "runtime": runtime,
                        "genre": self.format(genre, type="genre"),
                        "rating": self.format(rating, type="rating"),
                        "metascore": self.format(metascore, type="metascore"),
                        "description":self.format(description, type="description")
                    })
                print(Fore.GREEN + "INFO:       " + Fore.WHITE + f"[end pagination] - paging data {pagination} to {pagination + self.offset} catched")
                sleep(randint(2,10))
                pagination += self.offset
            print(Fore.GREEN + "INFO:   " + Fore.WHITE + f"[saving data] - saving {url['type']} data...")
            self.save_data(data, name_file=self.site + "_" + url["type"])
    
    def save_data(self, data: list[dict], name_file: str) -> None:
        with open("crawler/data/" + name_file + ".json","w") as file:
            json.dump(data,file,ensure_ascii=False,indent=2)