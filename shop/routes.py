import os
from flask import render_template, url_for, request, redirect, flash
from shop import app, db
from shop.models import Manufacturer, Phone, User
#from shop.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    phones = Phone.query.all()
    return render_template('home.html', phones=phones,)

@app.route("/about")
def about():
    return render_template('about.html', title='About us')

@app.route("/phone/<int:phone_id>")
def book(book_id):
    phone = phone.query.get_or_404(phone_id)
    return render_template('book.html', name=phone.name, phone=phone)
