from fastapi_camelcase import CamelModel
from typing import Optional
from datetime import datetime

class RunCrawler(CamelModel):
    offset: int
    site: str
    limit: int
    user: str
    password: str