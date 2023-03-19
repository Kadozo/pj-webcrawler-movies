from .Crawler import Crawler

OFFSET = 250
URL_TYPES = "imdbUrls"
LIMIT = 2500
NAME_FILE = "movies.json"
ROOT_FILE = "root.json"

Crawler(offset=OFFSET, urlTypes=URL_TYPES, limit=LIMIT, name_save_file=NAME_FILE).run(ROOT_FILE)