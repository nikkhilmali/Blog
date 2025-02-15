import os

import dotenv

dotenv.load_dotenv()


class Config:
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    DATABASE_PATH = os.getenv("DATABASE_PATH")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
