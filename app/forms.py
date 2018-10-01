from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,PasswordField,BooleanField, SelectField
from app.models import User
from wtforms.validators import DataRequired, Length,Email,EqualTo,ValidationError


class ToDO(FlaskForm):
    name = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    status = SelectField('Status', choices=[('New', 'New'),
                                                 ('In Progress', 'Progress'), ('Closed', 'Closed') ])
    submit = SubmitField('Submit')


class SignInForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    verify_password = PasswordField('Verify Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('SignUp')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Submit')
