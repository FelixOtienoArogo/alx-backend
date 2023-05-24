#!/usr/bin/env python3
"""
This module sets up a basic Flask app with localization support
using Flask-Babel.

It provides a Flask application instance, configures available languages,
default locale, and default timezone.
The app supports rendering HTML templates, handling HTTP requests,
and determining the best match for supported languages.
"""

from flask import Flask, render_template, request
from flask_babel import Babel, gettext
from typing import Tuple


class Config:
    """Configure available languages."""

    LANGUAGES: Tuple[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = "en"
    BABEL_DEFAULT_TIMEZONE: str = "UTC"


app: Flask = Flask(__name__)
"""Start flask app."""


app.config.from_object(Config)
"""Use that class as config for Flask app."""


babel: Babel = Babel(app)
"""Initialize babel."""


@babel.localeselector
def get_locale() -> str:
    """Determine the best match with our supported languages."""
    lang = request.args.get('locale')
    supplang = app.config['LANGUAGES']
    if lang in supplang:
        return lang
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def hello() -> str:
    """Just a test function."""
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(debug=True)
