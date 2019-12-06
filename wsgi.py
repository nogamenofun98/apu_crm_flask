from flask import Flask

app = Flask(__name__)  # because create_app() will use the app var so need to declare before it import

from app import create_app

create_app()  # initialize all things
if __name__ == "__main__":
    app.run(host='0.0.0.0')
