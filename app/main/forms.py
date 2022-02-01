from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired


class IdeaForm(FlaskForm):
    idea = StringField("Enter your idea", validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField("Submit")


class PortfolioForm(FlaskForm):
    title = StringField(
        "Enter your portfolio title", validators=[DataRequired(), Length(1, 128)]
    )
    submit = SubmitField("Submit")
