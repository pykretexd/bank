from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class CreateCustomerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email_address = StringField('Email Address', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    street_address = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    birthday = DateField('Date of Birth', validators=[DataRequired()])
    national_id = IntegerField('National ID', validators=[DataRequired()])
