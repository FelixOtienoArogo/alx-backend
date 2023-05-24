#!/usr/bin/env python3
""" Basic Flask app, Basic Babel setup, Get locale from request,
    Parametrize templates """
from flask import Flask, render_template, request
from flask_babel import Babel, gettext
from typing import Tuple


class Config:
    """ Configure available languages """

    LANGUAGES: Tuple[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = "en"
    BABEL_DEFAULT_TIMEZONE: str = "UTC"


app: Flask = Flask(__name__)
""" instantiate the app """


app.config.from_object(Config)
""" Use that class as config for Flask app """


babel: Babel = Babel(app)
""" instantiate the Babel object """


@babel.localeselector
def get_locale() -> str:
    """ to determine the best match with our supported languages """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def hello() -> str:
    """ basic Flask app """
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run(debug=True)
