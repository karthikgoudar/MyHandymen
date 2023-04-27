from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Role
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                role = Role.query.filter_by(id=user.role_id).first()
                flash("Logged in successfully as " + role.name + "!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", category="success")
    return redirect(url_for("views.home"))


@auth.route("/sign-up", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        roleid = request.form.get("usertype")

        if len(email) < 4:
            flash("Email must be greater than 4 characters.", category="error")
        elif len(first_name) < 3:
            flash('First-Name must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                flash("Email already exists.", category="error")
            else:
                role = Role.query.filter_by(id=roleid).first()
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'), role_id=roleid)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)
