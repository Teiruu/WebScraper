from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import InputRequired


class Scraper(FlaskForm):
    url = StringField('link_label',
                           validators=[InputRequired(message="Please enter a valid url")])
