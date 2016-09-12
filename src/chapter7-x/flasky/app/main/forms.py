from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

#表单
class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')