import os
from flask import render_template, url_for, request, redirect, flash
from shop import app, db
from shop.models import Manufacturer, Phone, User
from shop.forms import RegistrationForm , LoginForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    phones = Phone.query.all()
    return render_template('home.html', phones=phones)

@app.route("/about")
def about():
    return render_template('about.html', title='About us')

@app.route("/phone/<int:phone_id>")
def phone(phone_id):
    phone = Phone.query.get_or_404(phone_id)
    return render_template('phone.html', name=phone.model, phone=phone)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/Login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash("Sucessfully logged in")
            return redirect(url_for('home'))
        flash("Invalid username or password")

        return render_template('login.html', form=form)
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
