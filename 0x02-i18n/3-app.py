#!/usr/bin/env python3
"""
a python module to initiate a flask app using Babel
"""
from flask import Flask, render_template, request
from flask_babel import Babel, gettext
from typing import Tuple


class Config:
    """
    a class to configure babel
    """
    LANGUAGES: Tuple[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = "en"
    BABEL_DEFAULT_TIMEZONE: str = "UTC"


app: Flask = Flask(__name__)
app.config.from_object(Config)
babel: Babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    get_locale - function to get the local selector
    """
    lang = request.args.get('locale')
    supplang = app.config['LANGUAGES']
    if lang in supplang:
        return lang
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def hello() -> str:
    """
    hello - a route to a 4-index html
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(debug=True)
