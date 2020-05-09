from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, NewPostForm, Attack, Train
from app.models import User, Post, Monster



def create_monsters(user):
    M = {
        'username': 'Зомби',
        'xp': 10,
        'hp':10,
        'damage':10,
        'armor':0,
        'level':1,
        'money':1,
        'picture':'-',
    }

    monster = Monster(username=M['username'], xp=M['xp'], hp=M['hp'], 
        damage=M['damage'], armor=M['armor'], level=M['level'], money=M['money'], 
        picture=M['picture'], user_id=user.id)
    db.session.add(monster)
    db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)



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

        create_monsters(user)

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        print(form.body.data)
    return render_template('add_post.html', form=form)



@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user, monsters=monsters)


@app.route('/monster/<int:n>', methods=['GET', 'POST'])
@login_required
def monster(n):
    monster = Monster.query.filter(Monster.id == n).first()
    form = Attack()
    if form.validate_on_submit() and monster.hp > 0:
        monster.hp -= current_user.damage
        current_user.hp -= monster.damage - current_user.armor
        if current_user.hp <= 0:
            current_user.hp = 30
            current_user.xp = 0
            current_user.damage = 5
            current_user.armor = 0
            current_user.level = 0
            current_user.money = 10
            return "Вы умерли, начинаем все с начала!"
        if monster.hp <= 0:
            current_user.money += monster.money
            current_user.xp += monster.xp
            db.session.delete(monster)
            db.session.commit()
            create_monsters(current_user)
        db.session.commit() 
    return render_template('monster.html', monster=monster, form=form)


@app.route('/train', methods=['GET', 'POST'])
@login_required
def train():
    form = Train()
    if form.validate_on_submit():
        # res.set_cookie('user', 'train')
        # if n > 1000:
        current_user.damage += 1
        db.session.commit()
    res = render_template('train.html', form=form)
    return res


@app.route('/trader')
@login_required
def trader():
    return render_template('trader.html')

@app.route('/trader/heal', methods=['POST'])
@login_required
def heal():
    if current_user.money >= 5:
        current_user.money-=5
        current_user.hp += 5
        db.session.commit()
    return redirect('/trader')


@app.route('/trader/damage', methods=['POST'])
@login_required
def inc_damage():
    if current_user.money >= 5:
        current_user.money-=5
        current_user.damage += 5
        db.session.commit()
    return redirect('/trader')
@app.route('/monsters')
@login_required
def monsters():
    monsters = Monster.query.all()
    print(monsters)    
    return(monsters)

# flask db init 
# flask db migrate
# flask db upgrade
# flask run



