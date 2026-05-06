from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# MYSQL CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="kullu@200514",
    database="simple_local"
)

cursor = db.cursor(dictionary=True)


# SIGNUP PAGE + API
@app.route("/", methods=["GET", "POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Invalid Request"
        })

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "status": "error",
            "message": "All fields required"
        })

    hashed_password = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO users(name, email, password) VALUES(%s,%s,%s)",
            (name, email, hashed_password)
        )

        db.commit()

        return jsonify({
            "status": "success",
            "redirect": "/login"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


#  LOGIN PAGE + API
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Invalid Request"
        })

    email = data.get("email")
    password = data.get("password")

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if user and check_password_hash(user["password"], password):

        session["user"] = user["name"]

        return jsonify({
            "status": "success",
            "redirect": "/home"
        })

    return jsonify({
        "status": "error",
        "message": "Invalid Credentials"
    })



# HOME PAGE
@app.route("/home")
def home():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "home.html",
        name=session["user"]
    )


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)