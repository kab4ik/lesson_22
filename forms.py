# pip install flask-wtf
# pip install email_validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Email

class CommentForm(FlaskForm):
    author = StringField('имя: ', validators=[DataRequired()])
    email = StringField('email: ', validators=[Email()])
    text = TextAreaField('комментарий: ', validators=[DataRequired()])
    submit = SubmitField('Отправить')