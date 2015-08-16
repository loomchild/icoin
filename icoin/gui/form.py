from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, PasswordField, SubmitField, SelectField
from icoin.core.db import db
from icoin.core.model import User

class CreatePledgeForm(Form):
    url = StringField('URL')
    amount = SelectField('Amount', choices = [("1", "1€"), ("2", "2€")], default = '1')
    submit = SubmitField('Pledge')

class ClaimPageForm(Form):
    claim = SubmitField('Claim')
    cancel = SubmitField('Cancel')
