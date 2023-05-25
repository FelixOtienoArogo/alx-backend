#!/usr/bin/env python3
"""
a python module to initiate a flask app using Babel
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from datetime import timezone
from pytz import timezone
import pytz.exceptions


class Config(object):
    """
    a class to configure babel
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """
    get_locale - function to get the local selector
    """
    lang = request.args.get('locale', None)
    supplang = app.config['LANGUAGES']
    if lang in supplang:
        return lang
    if g.user:
        lang = g.user.get('locale')
        if lang in supplang:
            return lang
    lang = request.headers.get('locale', None)
    if lang in supplang:
        return lcl
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """
    get_timezone - function to get the timezone
    """
    timeZone = request.args.get('timezone', None)
    if timeZone:
        try:
            return timezone(timeZone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            return 'UTC'
    if g.user:
        try:
            timeZone = g.user.get('timezone')
            return timezone(timeZone).zone
        except pytz.exceptions.UnkownTimeZoneError:
            return 'UTC'
    default = app.cofig['BABEL_DEFAULT_TIMEZONE']
    return request.accept_languages.best_match(default)


@app.route('/', strict_slashes=False)
def hello():
    """
    hello - a route to a 4-index html
    """
    return render_template('6-index.html')


def get_user():
    """
    get_user - function that returns a given user
    """
    user_id = request.args.get('login_as', None)
    if user_id is None:
        return None
    return users.get(int(user_id))


@app.before_request
def before_request():
    """
    before_request - function to force execution before other methods
    """
    usr = get_user()
    g.user = usr


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
