import os

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, send_from_directory, get_flashed_messages
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import datetime
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

interests = [
    "Reading", "Photography", "Cooking", "Gardening", "Traveling", "Fishing", "Hiking",
    "Painting", "Music", "Dancing", "Writing", "Cycling", "Yoga", "Camping", "Running",
    "Swimming", "Rock climbing", "Skiing", "Snowboarding", "Chess", "Baking", "Knitting",
    "Pottery", "Woodworking", "Drawing", "Birdwatching", "Video gaming", "Fitness", "Running",
    "Meditation", "Stand-up comedy", "Journaling", "Astronomy", "Pottery", "Calligraphy",
    "Origami", "Beekeeping", "Surfing", "Sculpting", "Anime", "Fishing", "Bowling", "Football",
    "Basketball", "Baseball", "Soccer", "Tennis", "Table tennis", "Martial arts", "Boxing",
    "Fencing", "Weightlifting", "Parkour", "Sailing", "Motorcycling", "Horseback riding",
    "Gymnastics", "Snowshoeing", "Fencing", "Paddleboarding", "Snorkeling", "Diving",
    "Collecting stamps", "Collecting coins", "Collecting art", "Antiquing", "Restoring cars",
    "Restoring furniture", "DIY", "Home improvement", "Model building", "Origami", "Puzzles",
    "Escape rooms", "Board games", "Card games", "Billiards", "Darts", "Poker", "Scrapbooking",
    "Model trains", "Hockey", "Volleyball", "Rugby", "Cricket", "Badminton", "Archery",
    "Skateboarding", "Longboarding", "Rollerblading", "Sculpture", "Stained glass", "Tattooing",
    "Making jewelry", "Crocheting", "Candle making", "Soap making", "Sewing", "Embroidery",
    "Photography", "Photo editing", "Graphic design", "Web design", "Film making", "Documentary making",
    "Acting", "Directing", "Playwriting", "Improv", "Stand-up comedy", "Sketching", "Illustrating",
    "Bookbinding", "Leather crafting", "Glassblowing", "Printmaking", "Pottery", "Origami", "Zumba",
    "Ballet", "Salsa dancing", "Hip-hop dancing", "Tap dancing", "Breakdancing", "Ballroom dancing",
    "Hip-hop music", "Classical music", "Jazz music", "Rock music", "Pop music", "Rap music",
    "Reggae music", "Electronic music", "Opera", "Choral music", "Guitar playing", "Piano playing",
    "Drumming", "Singing", "Songwriting", "DJing", "Music production", "Playing ukulele", "Harmonica",
    "Violin playing", "Cello playing", "Flute playing", "Trumpet playing", "Clarinet playing",
    "Saxophone playing", "Tuba playing", "French horn playing", "Bass guitar", "Mandolin",
    "Bagpipes", "Music theory", "Learning languages", "Language exchange", "Public speaking",
    "Speech writing", "Storytelling", "Debating", "Model UN", "Volunteering", "Philanthropy",
    "Fundraising", "Activism", "Political campaigning", "Writing poetry", "Short story writing",
    "Essay writing", "Blogging", "Vlogging", "Podcasting", "Content creation", "Influencer marketing",
    "Digital marketing", "Social media", "Networking", "Event planning", "Travel writing", "Food writing",
    "Film criticism", "Art history", "Philosophy", "Psychology", "Sociology", "Anthropology",
    "Geography", "History", "Science", "Economics", "Technology", "Engineering", "Math", "Chemistry",
    "Physics", "Environmentalism", "Space exploration", "Artificial intelligence", "Machine learning",
    "Coding", "Programming", "App development", "Web development", "Data science", "Robotics",
    "Cybersecurity", "Blockchain", "Video editing", "Photography editing", "Virtual reality", "3D printing",
    "Augmented reality", "Podcast production", "Sound design", "Audio editing", "Graphic novels",
    "Webcomics", "Drawing comics", "Animation", "Stop-motion", "CGI", "Making memes", "Documenting history",
    "Genealogy", "Cultural exploration", "Sculpting", "Public art", "Mural painting", "Street art",
    "Museum visits", "Theater", "Cinema", "Live performances", "Comedy shows", "Opera watching",
    "Travel photography", "Food photography", "Fashion photography", "Architecture", "Interior design",
    "DIY furniture", "Upcycling", "Recycling", "Zero waste living", "Minimalism", "Sustainable living",
    "Organic gardening", "Herb gardening", "Fruit picking", "Preserving food", "Canning", "Brewery tours",
    "Wine tasting", "Whiskey tasting", "Coffee brewing", "Tea tasting", "Cheese making", "Baking bread",
    "Fermentation", "Culinary tourism", "Food blogging", "Gourmet cooking", "Healthy eating",
    "Cooking for kids", "Vegan cooking", "Vegetarian cooking", "Food photography", "Wine pairing",
    "Cooking classes", "Catering", "Cake decorating", "Cheese tasting", "Bartending", "Mixology",
    "Food science", "Herbalism", "Nutrition", "Dieting", "Farming", "Urban farming", "Aquaponics",
    "Beekeeping", "Animal rescue", "Adopting pets", "Training dogs", "Cat behavior", "Bird watching",
    "Pet photography", "Pet grooming", "Horseback riding", "Animal behavior", "Zoo visits", "Aquarium visits",
    "Bird watching", "Hiking with dogs", "Pet adoption", "Wildlife conservation", "Marine biology",
    "Environmental activism", "Sustainable fashion", "Fashion design", "Jewelry making", "Handbag design",
    "Shoe design", "Pattern making", "Cosplay", "Vintage fashion", "Luxury fashion", "Fashion photography",
    "Sewing", "Upcycling clothes", "Clothing repair", "Personal styling", "Wardrobe organizing", "Trend forecasting"
]

@app.route("/test")
def test():
    return render_template('index.html')

@app.route("/", methods=["GET"])
@login_required
def index():
    conn = sqlite3.connect('nexus.db')
    cur = conn.cursor()

    cur.execute(f"SELECT city, year FROM users WHERE id = {session["user_id"]}")
    rows = cur.fetchall()
    user_year = rows[0][1]
    user_city = rows[0][0].lower()


    year = datetime.date.today().strftime("%Y")

    #potential_friend_ids = []
    #for row in rows:
        #potential_friend_ids.append(row[0])
    #potential_friend_ids = list(set(potential_friend_ids))
    #placeholders = ', '.join(['?'] * len(potential_friend_ids))

    #cur.execute(f'''''', (user_year, user_year, user_city))
    #rows = cur.fetchall()

    #final_potential_friend_ids = []
    #for row in rows:
        #final_potential_friend_ids.append(row[0])

    #final_placeholders = ', '.join(['?'] * len(final_potential_friend_ids))
    cur.execute(f'''SELECT email, username, year, city, pfp FROM users WHERE id in (SELECT id FROM users 
                WHERE (year BETWEEN (? - 5) AND (? + 5) ) AND (city = ? COLLATE NOCASE))''', (user_year, user_year, user_city))
    rows = cur.fetchall()

    potential_friends = []

    for row in rows:
        new_friend = {}

        new_friend["email"] = row[0]
        new_friend["username"] = row[1]
        new_friend["age"] = int(year) - int(row[2])
        new_friend["city"] = row[3]
        new_friend["pfp"] = row[4]

        potential_friends.append(new_friend)

    cur.execute('''SELECT pfp FROM users WHERE id = ?''', str(session["user_id"]))
    user_pfp = cur.fetchall()[0][0]

    return render_template('index.html', potential_friends=potential_friends, user_pfp=user_pfp)
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
        if len(rows) != 1 or not check_password_hash(rows[0][1], request.form.get("password")):
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
            if not request.form.get(field):
                flash(f"Must enter {field}", 'error')
                return render_template("register.html")
        
        new_username = request.form.get("username")
        new_password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        year = request.form.get("year")
        email = request.form.get("email")
        city = request.form.get("city")
        pfp = request.files['pfp']

        filename = secure_filename(pfp.filename)
        filepath = os.path.join('static/images/pfps', filename)
        pfp.save(filepath)

        if new_password != confirmation:
            flash("Passwords must match", 'error')
            return render_template("register.html")
        
        conn = sqlite3.connect('nexus.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, username, hash, year, city, pfp) VALUES (?, ?, ?, ?, ?, ?)",
                    (email, new_username, generate_password_hash(new_password), int(year), city, filepath))
        conn.commit()

        
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
    session.pop("user_id")

    # Redirect user to login form
    return redirect("/")

@app.route("/enter_interests", methods=["GET"])
@login_required
def enter_interests():
    return render_template('enter_interests.html', interests=interests)

@app.route("/add_interest", methods=["POST"])
@login_required
def add_interest():
    flash("Successfully Added!", 'success')
    return redirect("/")

@app.route("/remove_interest", methods={"POST"})
@login_required
def remove_interest():
    pass





