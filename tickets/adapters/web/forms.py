from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import InputRequired, Regexp
from tickets.domain.entities import TicketType

from flask_security import RegisterForm


class OpenTicketForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    type = SelectField('Ticket Type', choices=[(item.name, item.value) for item in TicketType], validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])



class MyRegisterForm(RegisterForm):
    username = StringField('Username', validators=[InputRequired(), Regexp(r'[a-z0-9_]+')])
