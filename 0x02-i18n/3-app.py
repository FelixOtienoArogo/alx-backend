#!/usr/bin/env python3
"""Setup a basic Flask app."""
from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config:
    """Configure available languages."""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Determine the best match with our supported languages."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def hello():
    """Just a test function."""
    title = _("Welcome to Holberton")
    header = _("Hello world")
    return render_template('3-index.html', title=title, header=header)


if __name__ == '__main__':
    app.run(debug=True)
