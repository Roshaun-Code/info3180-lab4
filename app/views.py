import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import UserProfile
from app.forms import LoginForm, UploadForm

views = Blueprint('views', __name__)

def get_uploaded_images():
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    image_files = []
    
    if os.path.exists(upload_folder):
        for subdir, dirs, files in os.walk(upload_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_files.append(file)  
    
    return image_files

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/about/')
def about():
    return render_template('about.html', name="Mary Jane")

@views.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.getcwd(), 'uploads')

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        print(f"File saved to: {file_path}")  # Debug statement to confirm file path

        flash('File uploaded successfully!', 'success')
        return redirect(url_for('views.upload'))

    return render_template('upload.html', form=form)

@views.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = UserProfile.query.filter_by(username=username).first()

        if user and user.verify_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('views.upload'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=form)

@views.route('/files')
@login_required
def files():
    images = get_uploaded_images()
    print(f"Debug: Images list - {images}")  # Debug statement to check the images list
    return render_template('files.html', images=images)

@views.route('/uploads/<filename>')
def get_image(filename):
    upload_folder = os.path.abspath(os.path.join(os.getcwd(), 'uploads'))
    file_path = os.path.join(upload_folder, filename)
    
    # Debug: Print the upload folder and file path
    print(f"Debug: Upload folder - {upload_folder}")
    print(f"Debug: File path - {file_path}")
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Debug: File not found - {file_path}")
        abort(404)  # Return a 404 error if the file doesn't exist
    
    return send_from_directory(upload_folder, filename)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('views.home'))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in the {getattr(form, field).label.text} field - {error}", 'danger')

@views.route('/<file_name>.txt')
def send_text_file(file_name):
    file_dot_text = file_name + '.txt'
    return current_app.send_static_file(file_dot_text)

@views.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@views.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def init_app(app):
    app.register_blueprint(views)