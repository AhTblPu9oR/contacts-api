import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_NAME = os.getenv("DB_NAME", "contacts_db")

    # Pagination limits
    PRODUCTS_PER_PAGE = int(os.getenv("PRODUCTS_PER_PAGE", "10"))
    CONTACTS_PER_PAGE = int(os.getenv("CONTACTS_PER_PAGE", "20"))

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()