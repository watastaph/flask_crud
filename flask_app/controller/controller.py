from flask import render_template, flash,request, redirect, session
from flask_app import app
from flask_app.model.users import Users
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/users')
def users():
    user = Users.all_users()
    post = Users.all_post()
    return render_template("user.html", all_user = user, all_post = post)

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/add_user', methods=['POST'])
def add_user():
    if not Users.validate_user(request.form):
        return redirect('/users')
    
    pw_hash = bcrypt.generate_password_hash(request.form["txt-pword"])

    data = {
        "name" : request.form["txt-name"],
        "email" : request.form["txt-email"],
        "password" : pw_hash
    }

    Users.add_users(data)
    return redirect('/users')

@app.route('/delete_user/<user_id>')
def delete_user(user_id):
    data = {
        "id" : user_id
    }
    Users.delete_user(data)
    return redirect('/users')

@app.route('/retrieve_user/<user_id>')
def retrieve_user(user_id):
    data = {
        "id" : user_id
    }
    session['id'] = user_id
    user = Users.retrieve_user(data)
    return render_template('update.html', all_users = user)

@app.route('/update_user', methods=['POST'])
def update_user():
    pw_hash = bcrypt.generate_password_hash(request.form["txt-pword"])
    data = {
        "id" : session['id'],
        "name" : request.form["txt-name"],
        "email" : request.form["txt-email"],
        "password" : pw_hash
     }
    Users.update_user(data)
    return redirect('/users')

@app.route('/login_user', methods=['POST'])
def login_user():
    data = {
        "email" : request.form["txt-email"]
    }
    user_in_db = Users.login_user(data)
    if not user_in_db:
        flash("Invalid Username or Password")
        return redirect('/login')

    if not bcrypt.check_password_hash(user_in_db.password,  request.form["txt-pword"]):
        flash("Invalid Username or Password")
        return redirect('/login')

    session['user_id'] = user_in_db.id
    session['user_email'] = user_in_db.email
    session['user_name'] = user_in_db.name
    Users.login_user(data)
    return redirect('/users')

