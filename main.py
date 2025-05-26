#!.venv/bin/python
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from app import create_app

app: Flask = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

if __name__ == "__main__":
    app.run()
