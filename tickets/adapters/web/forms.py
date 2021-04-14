from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import InputRequired, AnyOf, ValidationError
from tickets.domain.entities import TicketType
from tickets.application.use_cases import check_username_exists


class OpenTicketForm(FlaskForm):
    author = StringField('Author', validators=[InputRequired()])
    title = StringField('Title', validators=[InputRequired()])
    type = SelectField('Ticket Type', choices=[(item.name, item.value) for item in TicketType], validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])

    def validate_author(self, field):
        if not check_username_exists(field._value()):
            raise ValidationError("Author is not registered")
