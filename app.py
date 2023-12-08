import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/talents')
def talents():
    return render_template('talents.html')


@app.route('/games')
def games():
    return render_template('games.html')


@app.route('/customer-summary')
def customer_summary():
    return render_template('/customer/summary.html')


@app.route('/customer-history')
def customer_history():
    return render_template('/customer/history.html')


@app.route('/talent-summary')
def talent_summary():
    return render_template('/talent/summary.html')


@app.route('/talent-history')
def talent_history():
    return render_template('/talent/history.html')


@app.route('/talent-orders')
def talent_orders():
    return render_template('/talent/orders.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
