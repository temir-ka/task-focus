from flask import (
    Blueprint, flash, redirect, render_template, url_for, request
)
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from .db import db, User
from sqlalchemy.exc import IntegrityError


bp = Blueprint('auth', __name__)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        

        if error is None:
            try:
                user = User(username=username)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                flash('Successfully registered', 'success')
                return redirect(url_for('auth.login'))
            except IntegrityError:
                db.session.rollback()
                flash('Username already exists.', 'danger')
                return redirect(url_for('auth.register'))
        flash(error, 'danger')
    return render_template('register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile.home'))  
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not user.check_password(password):
            error = 'Incorrect password.'
        
        if error is None:
            login_user(user)
            flash('Successfully logged in', 'success')
            return redirect(url_for('profile.home'))
        
        flash(error, 'danger')

    return render_template('login.html')
        

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out', 'success')
    return redirect(url_for('profile.home'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))