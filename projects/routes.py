from projects import app,db  
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify # type: ignore
from projects.forms import RegisterForm, LoginForm
from projects.models import User
from flask_login import login_user, logout_user, login_required # type: ignore

from projects.cat_and_dog import upload_image, predict_image
from projects.movie_rec import recommand, movies
from projects.mask_detector import mask_predict

app.config['UPLOAD_FOLDER'] = './static/images'  # Define your upload folder

@app.route('/')
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route('/models',methods=['GET', 'POST'])
@login_required
def models_page():
    return render_template('models.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=form.password1.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(attempted_pwd=form.password.data):
            login_user(user)
            flash(f'Success! U R Logged', category="success")
            return redirect(url_for('models_page'))
        else:
            flash('Invalid username or password', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", category='info')
    return redirect(url_for('home_page'))

# ------------------------------------------------------------------------------------------

@app.route('/cat_dog')
@login_required
def index_cat_dog():
    return render_template('cat_dog/index.html')

@app.route('/upload', methods=['POST'])
def upload_catdog_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = upload_image(file)
        if filename:
            return redirect(url_for('predict_catdog', filename=filename))
        flash('Error uploading file', category='danger')
    return redirect(url_for('index_cat_dog'))

@app.route('/predict/<filename>')
def predict_catdog(filename):
    prediction_label = predict_image(filename)
    return render_template('cat_dog/result.html', prediction=prediction_label)

# ------------------------------------------------------------------------------------------------


@app.route('/movies')
@login_required
def movies_home():
    return render_template('movie/recommand.html', movies=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form['movie_name']
    recommendations = recommand(movie_name)
    return jsonify(recommendations)

# --------------------------------------------------------------------------------------------------


@app.route('/mask')
@login_required
def mask_home():
    return render_template('mask/index.html')

@app.route('/upload_photo', methods=['POST'])
def upload_photo_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = upload_image(file)
        if filename:
            return redirect(url_for('predict_mask', filename=filename))
        flash('Error uploading file', category='danger')
    return redirect(url_for('mask_home'))

@app.route('/predict_mask/<filename>')
def predict_mask(filename):
    prediction_label = mask_predict(filename)
    return render_template('mask/result.html', prediction=prediction_label)







if __name__ == '__main__':
    app.run(debug=True)


