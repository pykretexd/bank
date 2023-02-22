from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class AccountIdForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Search')
