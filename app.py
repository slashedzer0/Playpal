import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import jwt
import datetime
import hashlib
import random
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
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = "./static/img/profiles"


@app.route('/')
def home():
    token = request.cookies.get("token")
    user_info = None
    talents = list(db.users.find({'role': 'talent'}, {
                   '_id': False, 'password': False}))
    shuffled_talents = random.sample(talents, 6)

    for talent in shuffled_talents:
        sum_rating = db.orders.find(
            {"talent": talent["username"], "rating": {"$exists": True}})
        total_rating = 0
        for rating in sum_rating:
            total_rating += int(rating["rating"])

        received_rating = db.orders.count_documents(
            {"talent": talent["username"], "rating": {"$exists": True}})
        overall_rating = total_rating / received_rating if received_rating != 0 else 0
        overall_rating = str(overall_rating)[:3]
        talent["ovr_rating"] = overall_rating

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    return render_template("index.html", user_info=user_info, talents=shuffled_talents)


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


@app.route('/profile/<username>')
def profile_page(username):
    token = request.cookies.get("token")
    user_info = None
    talent_info = db.users.find_one({"username": username})

    sum_rating = db.orders.find(
        {"talent": username, "rating": {"$exists": True}})
    total_rating = 0
    for rating in sum_rating:
        total_rating += int(rating["rating"])

    received_rating = db.orders.count_documents(
        {"talent": username, "rating": {"$exists": True}})
    overall_rating = total_rating / received_rating if received_rating != 0 else 0
    overall_rating = str(overall_rating)[:3]

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})

        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    return render_template("profile.html", user_info=user_info, talent_info=talent_info, overall_rating=overall_rating)


@app.route('/talents')
def talents_page():
    token = request.cookies.get("token")
    user_info = None

    talents = list(db.users.find({'role': 'talent'}, {
        '_id': False, 'password': False}))
    sorted_talents = sorted(talents, key=lambda x: x['fullname'].lower())

    for talent in talents:
        sum_rating = db.orders.find(
            {"talent": talent["username"], "rating": {"$exists": True}})
        total_rating = 0
        for rating in sum_rating:
            total_rating += int(rating["rating"])

        received_rating = db.orders.count_documents(
            {"talent": talent["username"], "rating": {"$exists": True}})
        overall_rating = total_rating / received_rating if received_rating != 0 else 0
        overall_rating = str(overall_rating)[:3]
        talent["ovr_rating"] = overall_rating

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    return render_template("talents.html", user_info=user_info, talents=sorted_talents)


@app.route('/games')
def games_page():
    token = request.cookies.get("token")
    user_info = None
    talents = list(db.users.find({'role': 'talent'}, {
                   '_id': False, 'password': False}))
    sorted_talents = sorted(talents, key=lambda x: x['fullname'].lower())

    for talent in talents:
        sum_rating = db.orders.find(
            {"talent": talent["username"], "rating": {"$exists": True}})
        total_rating = 0
        for rating in sum_rating:
            total_rating += int(rating["rating"])

        received_rating = db.orders.count_documents(
            {"talent": talent["username"], "rating": {"$exists": True}})
        overall_rating = total_rating / received_rating if received_rating != 0 else 0
        overall_rating = str(overall_rating)[:3]
        talent["ovr_rating"] = overall_rating

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login_page"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("login_page"))

    return render_template("games.html", user_info=user_info, talents=sorted_talents)


@app.route('/customer-summary')
def customer_summary_page():
    token = request.cookies.get("token")
    user_info = None

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_info = db.users.find_one({"username": payload["username"]})
            total_reviews = db.orders.count_documents(
                {"customer": user_info["username"], "status": "completed"})
            total_orders = db.orders.count_documents(
                {"customer": user_info["username"]})

            if user_info.get("role") != "customer":
                return redirect(url_for("home"))
            return render_template('/customer/summary.html', user_info=user_info, total_reviews=total_reviews, total_orders=total_orders)

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
            username = user_info["username"]

            quantity = db.orders.find({"talent": username, "status": {"$in": ["done", "completed"]}, "quantity": {
                "$exists": True}})
            total_quantity = 0
            for qty in quantity:
                total_quantity += int(qty["quantity"])

            total_income = int(user_info["price"]) * total_quantity
            received_orders = db.orders.count_documents(
                {"talent": user_info["username"]})

            sum_rating = db.orders.find(
                {"talent": username, "rating": {"$exists": True}})
            total_rating = 0
            for rating in sum_rating:
                total_rating += int(rating["rating"])

            received_rating = db.orders.count_documents(
                {"talent": username, "rating": {"$exists": True}})
            overall_rating = total_rating / received_rating if received_rating != 0 else 0
            overall_rating = str(overall_rating)[:3]

            if user_info.get("role") != "talent":
                return redirect(url_for("home"))
            return render_template('/talent/summary.html', user_info=user_info, overall_rating=overall_rating, total_income=total_income, received_orders=received_orders)

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
            received_orders = list(db.orders.find({'talent': user_info["username"], 'status': {'$ne': 'waiting'}}, {
                '_id': False}))

            if user_info.get("role") != "talent":
                return redirect(url_for("home"))
            return render_template('/talent/history.html', user_info=user_info, received_orders=received_orders)

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
    unit = request.form['unit']
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
        "unit": unit,
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


@app.route('/api/update_talent', methods=['POST'])
def update_talent():
    token = request.cookies.get('token')

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = payload['username']
        new_game = request.form['game']
        new_price = request.form['price']
        new_unit = request.form['unit']
        rank = request.form['rank']
        since = request.form['since']
        region = request.form['region']
        platform = request.form['platform']

        new_doc = {
            "game": new_game,
            "price": new_price,
            "unit": new_unit,
            "rank": rank,
            "since": since,
            "region": region,
            "platform": platform,
        }

        db.users.update_one({'username': username}, {'$set': new_doc})
        return jsonify({'result': 'success'})

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


@app.route('/api/load_customer_history')
def load_customer_history():
    token = request.cookies.get('token')

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            username = payload['username']
            created_orders = list(db.orders.find({'customer': username}, {
                '_id': False}))
            return jsonify({'result': 'success', 'created_orders': created_orders})

        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for('home'))


@app.route('/api/load_talent_orders')
def load_talent_orders():
    token = request.cookies.get('token')

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            username = payload['username']
            received_orders = list(db.orders.find({'talent': username, 'status': 'waiting'}, {
                '_id': False}))
            return jsonify({'result': 'success', 'received_orders': received_orders})

        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for('home'))


@app.route('/api/create_order', methods=['POST'])
def create_order():
    username_customer = request.form['customer']
    username_talent = request.form['talent']
    order_id = username_customer[:3] + datetime.now().strftime("%d%H%M%S")
    game = request.form['game']
    quantity = request.form['quantity']
    payment = request.form['payment']
    note = request.form['note']

    doc = {
        "customer": username_customer,
        "talent": username_talent,
        "order_id": order_id,
        "game": game,
        "quantity": quantity,
        "payment": payment,
        "note": note,
        "status": "waiting",
    }

    db.orders.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/api/add_rating', methods=['POST'])
def add_rating():
    token = request.cookies.get('token')

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            order_id = request.form['order_id']
            rating = request.form['rating']

            new_doc = {
                'rating': rating,
                'status': 'completed',
            }

            db.orders.update_one({'order_id': order_id}, {'$set': new_doc})
            return jsonify({'result': 'success'})

        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for('home'))


@app.route('/api/decline_order', methods=['POST'])
def decline_order():
    token = request.cookies.get('token')

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            order_id = request.form['order_id']
            db.orders.update_one({'order_id': order_id}, {
                '$set': {'status': 'declined'}})
            return jsonify({'result': 'success'})

        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for('home'))


@app.route('/api/approve_order', methods=['POST'])
def approve_order():
    token = request.cookies.get('token')

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            order_id = request.form['order_id']
            db.orders.update_one({'order_id': order_id}, {
                '$set': {'status': 'pending'}})
            return jsonify({'result': 'success'})

        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for('home'))


@app.route('/api/complete_order', methods=['POST'])
def complete_order():
    token = request.cookies.get('token')

    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

            order_id = request.form['order_id']
            print(order_id)
            db.orders.update_one({'order_id': order_id}, {
                '$set': {'status': 'done'}})
            return jsonify({'result': 'success'})

        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
            return redirect(url_for('home'))


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
