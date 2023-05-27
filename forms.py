from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField,PasswordField, SubmitField, IntegerField, FloatField, RadioField
from wtforms.validators import DataRequired


class ChildForm(FlaskForm):
    c_height = StringField("Child Height", validators=[DataRequired()])
    c_weight = FloatField("Child Weight", validators=[DataRequired()])
    c_age = FloatField("Child Age", validators=[DataRequired()])
    c_name = StringField("Address", validators=[DataRequired()])
    f_name = StringField("Address", validators=[DataRequired()])
    m_name = StringField("Address", validators=[DataRequired()])
    b_date = IntegerField('Phone Number', validators=[DataRequired()])
    gender = RadioField('Gender', choices=['Male', 'Female'], validators=[DataRequired()])
    p_number = IntegerField('Phone Number', validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    pin = IntegerField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Log Me In")


class APIRegistrationForm(FlaskForm):
    api_user = StringField("User Name", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register Me')


class AdminFrom(FlaskForm):
    admin_user = StringField('Admin User', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log Me In')
