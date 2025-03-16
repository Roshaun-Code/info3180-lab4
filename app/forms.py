from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class UploadForm(FlaskForm):
    file = FileField('Upload Image', validators=[
        FileRequired(),  # Ensure a file is uploaded
        FileAllowed(['jpg', 'png'], 'Only .jpg and .png files are allowed!')  # Allow only image files
    ])