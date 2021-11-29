import os


class Config:
    DEBUG = False
    TESTING = False
    DB_CONNECTOR = os.environ.get("DB_CONNECTOR")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")

    @property
    def DATABASE_URI(self):
        return "{connector}://{user}:{pwd}@{host}/{db}".format(
            connector=self.DB_CONNECTOR,
            user=self.DB_USER,
            pwd=self.DB_PASS,
            host=self.DB_HOST,
            db=self.DB_NAME,
        )


class ProductionConfig(Config):
    ENV = "production"


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    ENV = "testing"
    TESTING = True
    DEBUG = False
    DB_NAME = "book_test_db"
