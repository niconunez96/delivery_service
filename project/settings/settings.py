import os


class Config:
    DEBUG = False
    TESTING = False
    MONGO_HOST=os.environ.get("MONGO_HOST")
    MONGO_DB_NAME=os.environ.get("MONGO_DB_NAME")

    @property
    def MONGO_URI(self):
        return f"mongodb://{self.MONGO_HOST}/{self.MONGO_DB_NAME}"


class ProductionConfig(Config):
    ENV = "production"


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
