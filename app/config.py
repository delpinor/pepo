import os


def get_db_url():
    # if os.environ["APP_ENV"] == "DEV":
    #     return os.environ["DATABASE_URL_DEV"]
    return "postgresql://delpinor:cardenas@localhost:5432/pepo"
