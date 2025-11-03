from flask import Flask, redirect, render_template, request, jsonify
from cs50 import SQL
from datetime import datetime

app = Flask(__name__)

db = SQL("sqlite:///productivity.db") 

@app.route("/")
def index():
    return render_template("index.html")

