import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, send_from_directory, get_flashed_messages
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_required
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jyrfnhdg'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/test")
def test():
    return render_template('index.html')

@app.route("/", methods=["GET"])
@login_required
def index():
    conn = sqlite3.connect('nexus.db')
    cur = conn.cursor()
    cur.execute('''SELECT user_id FROM interests 
                WHERE (interest IN (SELECT interest FROM interests WHERE user_id = ?)''', session["user_id"])
    rows = cur.fetchall()

    potential_friend_ids = []
    for row in rows:
        potential_friend_ids.append(row[0])
    
    cur.execute('''SELECT ''')

    potential_friends = []

    for row in rows:
        new_friend = {}

        new_friend["email"] = row[0]
        new_friend["username"] = row[1]
        new_friend["age"] = 2024 - int(row[2])
        new_friend["city"] = row[3]

        potential_friends.append(new_friend)
    



    


    return render_template('index.html')
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must enter username", 'error')
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must enter password", 'error')
            return render_template("login.html")

        # Query database for username
        conn = sqlite3.connect('nexus.db')
        cur = conn.cursor()

        cur.execute("SELECT id, hash FROM users WHERE username = ?", (request.form.get("username"),))
        
        rows = cur.fetchall()
        cur.close()
        conn.close()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0][1], request.form.get("password")
        ):
            flash("Invalid username and/or password", 'error')
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        for field in ["email", "username", "password", "confirmation", "city", "year"]:
            print(field)
            if not request.form.get(field):
                flash(f"Must enter {field}", 'error')
                return render_template("register.html")
        
        new_username = request.form.get("username")
        new_password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        year = request.form.get("year")
        email = request.form.get("email")
        city = request.form.get("city")

        if new_password != confirmation:
            flash("Passwords must match", 'error')
            return render_template("register.html")
        
        conn = sqlite3.connect('nexus.db')
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (email, username, hash, year, city) VALUES (?, ?, ?, ?, ?)",
                       (email, new_username, generate_password_hash(new_password), int(year), city))
            conn.commit()
        except sqlite3.IntegrityError:
            flash("username/email is taken/already in use", 'error')
            return render_template("register.html")
        
        cur.close()
        conn.close()
        flash("Successfully registered!", 'success')
        return render_template('login.html')

    
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/enter_interests", methods=["GET"])
@login_required
def enter_interests():
    return render_template('enter_interests.html')

@app.route("/add_interest", methods=["POST"])
def add_interest():
    pass

@app.route("/remove_interest", methods={"POST"})
def remove_interest():
    pass





