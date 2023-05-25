#!/usr/bin/env python3
"""
a python module to initiate a Flask App
"""
from flask import Flask, render_template, request
from flask_babel import Babel, gettext
from typing import Tuple


class Config:
    """
    configure available languages
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
    determine the best match with our supported languages
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
    Just a test function
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(debug=True)
