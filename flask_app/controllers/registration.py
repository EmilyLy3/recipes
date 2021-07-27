from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models.user import User

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')

    else:
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }

    User.insert_user(data)

    flash("Registration successful! Please log in!")

    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email'],
    }

    user = User.get_users_by_email(data)

    # get_users_by_email() method returns a list, so if there is nothing in the list to match the email, this will redirect
    if not user:
        flash("Invalid email")
        return redirect('/')
    
    # if user is in the list, we can assign user_in_db to be the first list item (rather it should really be the ONLY list item) by assigning it index[0]
    user_in_db = user[0]

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid email/password")
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    session['user_first_name'] = user_in_db.first_name
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
