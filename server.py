import os
from typing import List, Optional
from flask import Flask, Blueprint
from werkzeug.utils import import_string

from project.settings.settings import Config
from project.database import db, mongo_client
from project.controller import delivery, costumer_address
from project.rabbitmq import initAuth, initDomainListeners


class AppBuilder:
    app: Flask
    config_instance: Config

    def __init__(self, import_name: str, setting: Optional[str] = None):
        self.config_instance = import_string(setting)() if setting else None
        self.app = Flask(import_name)
        self.app.config.from_object(self.config_instance)

    def add_configuration(self, setting: str) -> None:
        self.config_instance = import_string(setting)()
        self.app.config.from_object(self.config_instance)

    def add_endpoints(self, endpoints: List[Blueprint]) -> None:
        for endpoint in endpoints:
            self.app.register_blueprint(endpoint)

    def add_database(self) -> None:
        self.app.config['SQLALCHEMY_DATABASE_URI'] \
            = self.config_instance.DATABASE_URI
        self.app.config['MONGO_URI'] = "mongodb://localhost:27017/delivery"
        # silence the deprecation warning
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def build(self) -> Flask:
        return self.app


app_builder = AppBuilder(__name__, os.environ.get("ENV_CONFIG"))
app_builder.add_endpoints([delivery, costumer_address])
app_builder.add_database()

app = app_builder.build()
db.init_app(app)
mongo_client.init_app(app)
initAuth()
initDomainListeners()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
