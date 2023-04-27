from flask import Blueprint, render_template, flash, request, redirect, url_for, send_file
from flask_login import login_required, current_user
from .models import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from io import BytesIO
import base64
from types import SimpleNamespace


views = Blueprint("views", __name__)


@views.route("/")
def home():
    handyMenInfo = HandymanInfo.query.all()
    handymen = []
    for handyman in handyMenInfo:
        handyManInfo = SimpleNamespace(
                firstname1 = handyman.firstname1,
                lastname1 = handyman.lastname1,
                price_per_hour = handyman.price_per_hour,
                gender = handyman.gender,
                professioncategory = handyman.professioncategory,
                email1 = handyman.email1,
                phone = handyman.phone,
                description = handyman.description,
                user_id = handyman.user_id,
                profileImage = base64.b64encode(handyman.profileimage).decode("utf-8") if handyman.profileimage else None
        )
        handymen.append(handyManInfo)
        
    return render_template("home.html", user=current_user, handymen=handymen)


@views.route("/profile")
def profile():
    handyman = HandymanInfo.query.filter_by(user_id=current_user.id).first()
    profileImage = None
    if handyman:
        profileImage = base64.b64encode(handyman.profileimage).decode("utf-8")
    return render_template("profile.html", user=current_user, handymaninfo=handyman, profileimage = profileImage)

@views.route("/editprofile", methods=["GET", "POST"])
def update_profile():
    if request.method == "POST":
        firstname1 = request.form.get("firstname1")
        lastname1 = request.form.get("lastname1")
        professionid = request.form['profession']
        price_per_hour = request.form.get("price")
        gender = request.form['gender']
        email1 = request.form.get("email1")
        phone = request.form.get("phone")
        description = request.form.get("description")
        profileImage = request.files["profileImage"]
        profileImageBinary = profileImage.read()

        if len(firstname1) < 4:
            flash("First Name must be greater than 4 characters", category="error")
        elif len(lastname1) < 4:
            flash("Last Name must be greater than 4 characters", category="error")
        elif len(price_per_hour) < 2:
            flash("Enter a valid price", category="error")
        elif professionid == None:
           flash("Please select a profession", category="error")
        elif gender == None:
           flash("Please select a gender", category="error")
        elif len(email1) < 4:
            flash("Email must be greater than 4 characters", category="error")
        elif len(phone) != 10:
            flash("Enter a valid phone number", category="error")
        elif len(description) < 10:
            flash("Description must be greater than 10 characters", category="error")

        else:
            handyman = HandymanInfo.query.filter_by(user_id=current_user.id).first()
            professionCategory = HandymanProfessionCategory.query.with_entities(HandymanProfessionCategory.category).filter_by(id=professionid).first().category
            if handyman:
                handyman.firstname1 = firstname1
                handyman.lastname1 = lastname1
                handyman.price_per_hour = price_per_hour
                handyman.gender = gender
                handyman.professioncategory = professionCategory
                handyman.email1 = email1
                handyman.phone = phone
                handyman.description = description
                handyman.user_id = current_user.id
                handyman.profileimage = profileImageBinary
                profileImage = base64.b64encode(handyman.profileimage).decode("utf-8")
                db.session.commit()
                return render_template("profile.html", user=current_user, handymaninfo=handyman, profileimage = profileImage)
            else:
                new_handyman = HandymanInfo(firstname1=firstname1, lastname1=lastname1, price_per_hour=price_per_hour, gender = gender,
                                            professioncategory=professionCategory, email1=email1, phone=phone, description=description, 
                                            user_id=current_user.id, profileimage=profileImageBinary)
                db.session.add(new_handyman)
                db.session.commit()
                flash("Profile successfully updated!", category="success")
                profileImage = base64.b64encode(new_handyman.profileimage).decode("utf-8")
                return render_template("profile.html", user=current_user, handymaninfo=new_handyman, profileimage = profileImage)

        return render_template("editprofile.html", user=current_user)
    else:
        handyman = HandymanInfo.query.filter_by(user_id=current_user.id).first()
        handymanCategories = HandymanProfessionCategory.query.all()
        #profileImage = base64.b64encode(handyman.profileimage).decode("utf-8")
        return render_template("editprofile.html", user=current_user, handymanCategories=handymanCategories, handymanInfo=handyman)
