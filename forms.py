from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

def CountryCode(form, field):
    if len(field.data) != 2:
        raise ValidationError('Country code must be 2 characters.')

def NationalId(form, field):
    if len(field.data) < 12:
        raise ValidationError('National ID must be 12 characters.')

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

class WithdrawForm(FlaskForm):
    account = SelectField('Which account would you like to withdraw from?', choices=[], validators=[DataRequired()])
    amount = IntegerField('How much would you like to withdraw?', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class DepositForm(FlaskForm):
    account = SelectField('Which account would you like to deposit to?', choices=[], validators=[DataRequired()])
    amount = IntegerField('How much would you like to deposit?', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class TransferForm(FlaskForm):
    account = SelectField('Which account would you like to transfer from?', choices=[], validators=[DataRequired()])
    target = IntegerField('Enter ID of account to transfer to.', validators=[DataRequired()])
    amount = IntegerField('How much would you like to transfer?', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class LoginUserForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SignupUserForm(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

class UpdateCustomerForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email_address = StringField('Email Address', validators=[Email()])
    telephone_country_code = IntegerField('Telephone Country Code')
    phone_number = StringField('Phone Number')
    street_address = StringField('Street Address')
    city = StringField('City')
    country = StringField('Country')
    country_code = StringField('Country Code', validators=[CountryCode])
    zipcode = IntegerField('ZIP code')
    birthday = DateField('Date of Birth')
    national_id = StringField('National ID (XXXXXXXX-XXXX)', validators=[NationalId])
    submit = SubmitField('Submit')

class UpdateUserForm(FlaskForm):
    email_address = StringField('Email Address')
    role = SelectField('Role', choices=[])
    submit = SubmitField('Submit')
