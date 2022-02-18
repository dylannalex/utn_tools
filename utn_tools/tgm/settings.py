import os

TOKEN = os.getenv("TOKEN")
MODE = os.getenv("MODE")
PORT = int(os.environ.get("PORT", "8443"))
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
SHOW_SURVEY_EXCEPTIONS = bool(os.getenv("SHOW_SURVEY_EXCEPTIONS"))
