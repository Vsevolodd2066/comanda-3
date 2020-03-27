from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, NewPostForm
from app.models import User, Post, Monster


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.all()

    return render_template('index.html', title='Home', posts=posts)

@app.route('/my_posts')
@login_required
def my_posts():
    posts = Post.query.filter_by(user_id=current_user.id)

    return render_template('index.html', title='My', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def me():
    return render_template('add_post.html', form=form)

@app.route("/profile")
@login_required
def profile():
	hp = current_user.hp
	return "<h1>Profile page!</h1>"+str(hp)

@app.route('/monster/<int:n>')
@login_required
def monster(n):
    monster = Monster.query.filter(Monster.id == n).first()
    return str(monster.hp)
# flask db init 
# flask db migrate
# flask db upgrade
# flask run
