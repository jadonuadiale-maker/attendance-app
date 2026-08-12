from flask import Blueprint, render_template, request, redirect, url_for, session
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(full_name=username).first()
    if not user or not user.check_password(password):
        return render_template("login.html", error="Invalid credentials")

    session["user_id"] = user.id
    session["role"] = user.role
    session["classgroup_id"] = user.classgroup_id
    return redirect(url_for("dashboard"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))
