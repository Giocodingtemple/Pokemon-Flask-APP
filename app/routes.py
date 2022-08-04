from flask import render_template, request, redirect, url_for, flash
from app import app
from .forms import LoginForm, RegisterForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required

#Routes
@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@app.route('/pokeapi', methods=['GET','POST'])
def pokeapi():
    if request.method == 'POST':
        id = request.form.get('id')

        url =  f'https://pokeapi.co/api/v2/pokemon/{id}.json'
        response = request.get(url)
        if not response.ok:
            error_string = 'We had an error'
            return render_template('pokeapi.html.j2', error=error_string)

        if not response.json():
            error_string = "We had an error loading your data most likely because the id combo is not in the database"
            return render_template('pokeapi.html.j2', error=error_string)

        data = response.json()
        new_data = []
        for pokemon in data:
            pokemon_dict={}
            pokemon_dict={
                "pokemon-name":pokemon['pokemon']['name'],
                "pokemon-ability":pokemon['pokemon-ability'],
                "pokemon-defense-base-stat":pokemon['pokemon-defense-base-stat'],
                "pokemon-attack-base-stat":pokemon['pokemon-attack-base-stat'],
                "pokemon-hp-base-stat":pokemon['pokemon-hp-base-stat'],
                "pokemon-sprite":pokemon['pokemon-sprite']
            }
            new_data.append(pokemon_dict)
        
        return render_template('pokeapi.html.j2', pokemon=new_data)
    return render_template('pokeapi.html.j2')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data,
                "icon":form.icon.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            error_string="There was a problem creating your account. Please try again"
            return render_template('register.html.j2',form=form, error=error_string)
        return redirect(url_for('login'))

    return render_template('register.html.j2',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        u = User.query.filter_by(email=email).first()
        print(u)
        if u is not None and u.check_hashed_password(password):
            login_user(u)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    return render_template("login.html.j2", form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user is not None:
        logout_user()
        return redirect(url_for('index'))
