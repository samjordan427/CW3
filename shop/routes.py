import os
from flask import rener_template, url_for, request, redirect, flash
from shop import app, debug
#from shop.models import add in the database tables
from shop.forms import RegistrationForm, LoginForm
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user, logout_user, login_required
