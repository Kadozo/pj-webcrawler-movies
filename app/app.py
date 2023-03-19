from .config.db import init_db
from .config.middlewares import init_middleware
from .config.routes import init_routes
from .config.app import get_app
import sys

args = sys.argv

"""Initializing app"""
app = get_app()

"""Including routes in App"""
init_routes(app)

"""Including middlewares in App"""
init_middleware(app)

"""Initializing Database"""
if((len(args) < 1) and (args[1] != "--init-db")):
    init_db(app)