from uvicorn import run
from app.config.settings import getSettings

settings = getSettings()

if __name__ == "__main__":
    run("app.app:app", host="0.0.0.0", port=settings.APP_PORT, log_level="info", reload=True)