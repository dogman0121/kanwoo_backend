from kanwoo import create_app
from config import config

app = create_app(config)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)