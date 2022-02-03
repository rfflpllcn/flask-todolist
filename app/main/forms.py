from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SearchField, SelectField
from wtforms.validators import Length, DataRequired

# from app.models import Instrument


class IdeaForm(FlaskForm):
    description = StringField("Enter your invest idea name",
                              validators=[DataRequired(),
                                          Length(1, 128)])
    isin = SelectField("Choose your invest idea ISIN",
                       validators=[DataRequired()]
                       )
    submit = SubmitField("Submit")


class PortfolioForm(FlaskForm):
    title = StringField(
        "Enter your portfolio title", validators=[DataRequired(), Length(1, 128)]
    )
    submit = SubmitField("Submit")
