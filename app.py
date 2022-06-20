import logging
from flask import Flask
from const import MAX_CONTENT_LENGTH
from main.views import main_blueprint
from loader.views import loader_blueprint

logging.basicConfig(filename="log.log", level=logging.INFO)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

app.register_blueprint(main_blueprint)
app.register_blueprint(loader_blueprint)

if __name__ == '__main__':
    app.run()
