import os
from flask import render_template, url_for, request, redirect, flash, session
from shop import app, db
from shop.models import Manufacturer, Phone, User
from shop.forms import RegistrationForm , LoginForm, CheckoutForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    phones = Phone.query.all()
    return render_template('home.html', phones=phones,title="Phone Hub")

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

@app.route("/add_to_cart/<int:phone_id>")
def add_to_cart(phone_id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(phone_id)
    flash("The phone has been added to your shopping cart!")
    return redirect("/cart")

@app.route("/cart", methods=['GET', 'POST'])
def cart_display():
    if "cart" not in session:
        flash('There is nothing in your cart.')
        return render_template("cart.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        cart = {}

        total_price = 0
        total_quantity = 0
        for item in items:
            phone = Phone.query.get_or_404(item)

            total_price += phone.price
            if phone.id in cart:
                cart[phone.id]["quantity"] += 1
            else:
                cart[phone.id] = {"quantity":1, "product": phone.model, "price":phone.price}
            total_quantity = sum(item['quantity'] for item in cart.values())

        return render_template("cart.html", title='Your Shopping Cart', display_cart = cart, total = total_price, quantity = total_quantity)

    return render_template('cart.html')

@app.route("/delete_phone/<int:phone_id>", methods=['POST'])
def delete_phone(phone_id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].remove(phone_id)
    flash("The phone has been removed from your shopping cart!")
    session.modified = True

    return redirect("/cart")

@app.route("/checkout")
def checkout():
    items = session["cart"]
    cart = {}
    form = CheckoutForm()

    total_price = 0
    total_quantity = 0
    for item in items:
        phone = Phone.query.get_or_404(item)

        total_price += phone.price
        if phone.id in cart:
            cart[phone.id]["quantity"] += 1
        else:
            cart[phone.id] = {"quantity":1, "Product": phone.model, "price":phone.price}
        total_quantity = sum(item['quantity'] for item in cart.values())
    return render_template('checkout.html', title='Payment', total=total_price, form=form)
