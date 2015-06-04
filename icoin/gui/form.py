from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, PasswordField, SubmitField, SelectField
from wtforms.validators import ValidationError, Required, Email, Length, Regexp, EqualTo


class LoginForm(Form):
    email = StringField('Email', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Log In')

class CreatePledgeForm(Form):
    url = StringField('URL')
    amount = SelectField('Amount', choices = [("1", "1€"), ("2", "2€")], default = '1')
    submit = SubmitField('Submit')

class ClaimPageForm(Form):
    yes = SubmitField('Yes')
    no = SubmitField('No')
