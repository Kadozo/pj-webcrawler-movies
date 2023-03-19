from Crawler import Crawler

OFFSET = 250
SITE = "imdb"
LIMIT = 2500
ROOT_FILE = "crawler/root.json"

Crawler(offset=OFFSET, site=SITE, limit=LIMIT).run(ROOT_FILE)