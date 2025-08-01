from flask import redirect, render_template, url_for, flash, jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
from base64 import b64encode, b64decode
from .forms import RegisterForm, LoginForm, NewPassForm
from .models import User, Password
from .db import db
from .key_generator import generate_key, regenerate_key
from .cipher import cipher_pass, decipher_pass
from . import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET","POST"])
def show_signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.master_key.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Creaste tu cuenta correctamente", category="success")
        return redirect(url_for("index"))
    if form.errors != {}:
        for err_msg in form.errors:
            flash(f"Hubo un error creando la cuenta: {err_msg}", category="danger")
    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET","POST"])
def show_login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password(attempted_password=form.master_key.data):
            login_user(attempted_user)
            flash(f"Has ingresado a tu cuenta como {attempted_user.username}", category="success")
            return redirect(url_for("show_accounts"))
        else:
            flash(f"Tu correo y/o contraseña son inválidos", category="danger")    
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("Has salido de tu cuenta", category="info")
    return redirect(url_for("index"))

@app.route("/accounts")
def show_accounts():
    if current_user.is_authenticated:
        passwords = current_user.passwords
        return render_template("accounts.html", passwords=passwords)
    else:
        return render_template("notallowed.html")

@app.route("/new-pass", methods=["GET","POST"])
def new_pass():
    form = NewPassForm()
    if form.validate_on_submit():
        service = form.service.data
        password = form.password.data
        link = form.link.data
        key, salt = generate_key(current_user.hashed_master_key.decode('utf-8'))
        ct, iv = cipher_pass(password, key)
        new_password = Password(service=service, link=link,cipher_pass=ct, iv=iv, salt=b64encode(salt).decode('utf-8'), user_id=current_user.id)
        db.session.add(new_password)
        db.session.commit()
        return redirect(url_for("show_accounts"))
    return render_template("newpass.html", form=form)

@app.route("/accounts/<int:id>", methods=["GET"])
@login_required
def get_pass(id):
    password = Password.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    ct = password.cipher_pass
    iv = password.iv
    salt = b64decode(password.salt)
    key = regenerate_key(current_user.hashed_master_key.decode('utf-8'), salt)
    plain_password = decipher_pass(ct, iv, key)
    return jsonify({"password":plain_password})

@app.route("/accounts/<int:id>/edit", methods=["GET","POST"])
@login_required
def edit_pass(id):
    password = Password.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    if request.method == "POST":
        password.service = request.form["service"]
        new_plain_password = request.form["password"]
        key, salt = generate_key(current_user.hashed_master_key.decode('utf-8'))
        ct, iv = cipher_pass(new_plain_password, key)
        password.cipher_pass = ct
        password.salt = b64encode(salt).decode('utf-8')
        password.iv = iv
        password.link = request.form["link"]
        db.session.commit()
        return redirect(url_for("show_accounts"))
    return render_template("edit.html", password=password)


@app.route("/accounts/<int:id>/delete", methods=["GET","POST"])
@login_required
def delete_pass(id):
    password = Password.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(password)
    db.session.commit()
    return redirect(url_for("show_accounts"))

@app.route("/my-account", methods=["GET","POST"])
@login_required
def my_account():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        
        current_user.username = username
        current_user.email = email
        db.session.commit()
    return render_template("myaccount.html")
