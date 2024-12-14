from flask import Flask, render_template, request, send_from_directory, flash, get_flashed_messages, redirect
from firebase import firebase

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response










