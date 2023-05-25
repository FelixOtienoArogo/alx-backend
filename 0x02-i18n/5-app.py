#!/usr/bin/env python3
"""
This module sets up a basic Flask app with localization support
using Flask-Babel.

It provides a Flask application instance, configures available languages,
default locale, and default timezone.
The app supports rendering HTML templates, handling HTTP requests,
and determining the best match for supported languages.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext
from typing import Tuple, Dict


class Config:
    """Configure available languages."""

    LANGUAGES: Tuple[str] = ["en", "fr"]
    BABEL_DEFAULT_LOCALE: str = "en"
    BABEL_DEFAULT_TIMEZONE: str = "UTC"


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}
    

app: Flask = Flask(__name__)


app.config.from_object(Config)
"""Use that class as config for Flask app."""


babel: Babel = Babel(app)


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
    return render_template('5-index.html')


def get_user() -> Dict:
    """Return a user dictionary or None if the ID cannot be found."""
    try:
        userId = request.args.get('login_as')
        return users[int(userId)]
    except Exception:
        return None


@app.before_request
def before_request() -> None:
    """Use get_user to find a user if any, and set it as a global."""
    g.user = get_user()


if __name__ == '__main__':
    app.run(debug=True)
