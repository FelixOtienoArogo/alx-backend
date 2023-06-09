#!/usr/bin/env python3
"""Setup a basic Flask app."""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configure available languages."""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route('/')
def hello():
    """Just a test function."""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(debug=True)
