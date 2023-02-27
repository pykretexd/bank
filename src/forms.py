from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email

def CountryCode(form, field):
    if len(field.data) != 2:
        raise ValidationError('Country code must be 2 characters.')

class CreateCustomerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    telephone_country_code = IntegerField('Telephone Country Code', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    street_address = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    country_code = StringField('Country Code', validators=[DataRequired(), CountryCode])
    zipcode = IntegerField('ZIP code', validators=[DataRequired()])
    birthday = DateField('Date of Birth', validators=[DataRequired()])
    national_id = StringField('National ID (XXXXXXXX-XXXX)', validators=[DataRequired()])
    submit = SubmitField('Submit')
