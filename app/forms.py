from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):

    username = StringField(label="Nombre de usuario:", validators=[Length(min=3, max=20), DataRequired()])
    master_key = PasswordField(label="Clave maestra", validators=[Length(min=8), DataRequired()])
    email = EmailField(label="Email:", validators=[Email(), DataRequired()])
    submit = SubmitField(label="Crear cuenta")


class LoginForm(FlaskForm):

    email = EmailField(label="Email:", validators=[DataRequired()])
    master_key = PasswordField(label="Clave maestra", validators=[DataRequired()])
    submit = SubmitField(label="Ingresar")

class NewPassForm(FlaskForm):

    service = StringField(label="Servicio:", validators=[Length(min=2), DataRequired()])
    password = PasswordField(label="Contraseña:", validators=[Length(min=8), DataRequired()]) 
    link = StringField(label="Link:", validators=[DataRequired()])
    submit = SubmitField(label="Crear contraseña")