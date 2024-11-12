from flask import Flask
from routes.route import main
from database.db import Database
from config.settings import Config
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)

    url_model = Database()
    url_model.init_db()

    app.register_blueprint(main)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
