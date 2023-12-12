import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import jwt
import datetime
import hashlib
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = "PLAYPAL"

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
app = Flask(__name__)


@app.route('/')
def home():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    return render_template("index.html", user_info=user_info)


@app.route('/register')
def register_page():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})

            if user_info:
                return redirect(url_for("home"))
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    return render_template("register.html", user_info=user_info)


@app.route('/login')
def login_page():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})

            if user_info:
                return redirect(url_for("home"))
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    return render_template("login.html", user_info=user_info)


@app.route('/profile')
def profile_page():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    return render_template("profile.html", user_info=user_info)


@app.route('/talents')
def talents_page():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    return render_template("talents.html", user_info=user_info)


@app.route('/games')
def games_page():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    return render_template("games.html", user_info=user_info)


@app.route('/customer-summary')
def customer_summary_page():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})

            if user_info.get("role") != "customer":
                return redirect(url_for("home"))
            return render_template('/customer/summary.html', user_info=user_info)

        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for("login_page"))

    return redirect(url_for("home"))


@app.route('/customer-history')
def customer_history_page():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})

            if user_info.get("role") != "customer":
                return redirect(url_for("home"))
            return render_template('/customer/history.html', user_info=user_info)

        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    else:
        return redirect(url_for("home"))


@app.route('/talent-summary')
def talent_summary_page():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})

            if user_info.get("role") != "talent":
                return redirect(url_for("home"))
            return render_template('/talent/summary.html', user_info=user_info)

        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    else:
        return redirect(url_for("home"))


@app.route('/talent-history')
def talent_history_page():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})

            if user_info.get("role") != "talent":
                return redirect(url_for("home"))
            return render_template('/talent/history.html', user_info=user_info)

        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    else:
        return redirect(url_for("home"))


@app.route('/talent-orders')
def talent_orders_page():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})

            if user_info.get("role") != "talent":
                return redirect(url_for("home"))
            return render_template('/talent/orders.html', user_info=user_info)

        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    else:
        return redirect(url_for("home"))


@app.route('/api/register_customer', methods=['POST'])
def register_customer():
    fullname = request.form['fullname']
    username = request.form['username']
    password = request.form['password']
    exists = bool(db.users.find_one({"username": username}))

    if exists:
        return jsonify({'result': 'failed', 'exists': exists})

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    doc = {
        "fullname": fullname,
        "username": username,
        "password": password_hash,
        "pfp_new": "",
        "pfp_default": "img/profiles/profile-pic.jpg",
        "role": "customer",
    }

    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/api/register_talent', methods=['POST'])
def register_talent():
    fullname = request.form['fullname']
    username = request.form['username']
    password = request.form['password']
    game = request.form['game']
    price = request.form['price']
    exists = bool(db.users.find_one({"username": username}))

    if exists:
        return jsonify({'result': 'failed', 'exists': exists})

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    doc = {
        "fullname": fullname,
        "username": username,
        "password": password_hash,
        "game": game,
        "price": price,
        "pfp_new": "",
        "pfp_default": "img/profiles/profile-pic.jpg",
        "role": "talent",
    }

    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route("/api/login", methods=["POST"])
def login_verification():
    username = request.form["username"]
    password = request.form["password"]
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    result = db.users.find_one(
        {
            "username": username,
            "password": password_hash,
        }
    )

    if result:
        payload = {
            "username": username,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"result": "success", "token": token})

    else:
        return redirect(url_for("login_page"))


@app.route('/api/update_account', methods=['POST'])
def update_account():
    token = request.cookies.get('token')

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = payload['username']
        new_fullname = request.form['fullname']
        new_username = request.form['username']
        new_doc = {'fullname': new_fullname, 'username': new_username}

        if 'avatar' in request.files:
            avatar = request.files['avatar']
            filename = secure_filename(avatar.filename)
            extension = filename.split('.')[-1]
            file_path = f'img/profiles/{new_username}.{extension}'
            avatar.save('./static/' + file_path)
            new_doc['pfp_new'] = filename
            new_doc['pfp_default'] = file_path

        payload['username'] = new_username
        new_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        db.users.update_one({'username': username}, {'$set': new_doc})

        response = jsonify({'result': 'success'})
        response.set_cookie('token', new_token)
        return response

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for('home'))


@app.route('/api/delete_account', methods=['POST'])
def delete_account():
    token = request.cookies.get('token')

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})
            db.users.delete_one({"username": user_info["username"]})
            return jsonify({'result': 'success'})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
