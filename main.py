from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "sikrit"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)

credential_masteruser = "ARISAKA"
credential_password = "Snipg21jaJs"

db = SQLAlchemy(app)

class PasswordEntries(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    platformName = db.Column("platformName", db.String(20))
    accountTag = db.Column("accountTag", db.String(30))
    tagType = db.Column("tagType", db.String(20))
    phoneNumber = db.Column("phone", db.String(15))
    password = db.Column("password", db.String(50))
    otherData = db.Column("otherData", db.String(150))
    otherDataType = db.Column("otherDataType", db.String(20))
    def __init__(self, platformName, accountTag, tagType, phoneNumber, password, otherData, otherDataType):
        self.platformName = platformName
        self.accountTag = accountTag
        self.tagType = tagType
        self.phoneNumber = phoneNumber
        self.password = password
        self.otherData = otherData
        self.otherDataType = otherDataType


@app.route("/")
def index():
    return redirect(url_for('master_login'))

@app.route("/masterlogin", methods = ["GET", "POST"])
def master_login():
    if 'user' in session:
        return redirect(url_for("view"))
    if request.method == "POST":
        if request.form['uname'] != credential_masteruser:
            return "Access Denied"
        if request.form['mpw'] != credential_password:
            return "Access Denied"
        else:
            session['user'] = credential_masteruser
            return redirect(url_for("view"))
    return render_template("master_login.html")

@app.route("/view")
def view():
    if 'user' in session:
        entries = PasswordEntries.query.limit(50).all()
        return render_template("view.html", entries=entries)
    else:
        redirect(url_for('master_login'))

@app.route("/edit", methods = ["POST"])
def edit():
    #Find and check existance
    found_user = PasswordEntries.query.filter_by(platformName=request.form['platform'], accountTag=request.form['account']).first()
    if found_user is None:
        pass
    else:
        oldPlatform = found_user.platformName
        oldTag = found_user.accountTag
        found_user.accountTag = request.form['account']
        found_user.tagType = request.form['account_type']
        found_user.phoneNumber = request.form['phone']
        found_user.password = request.form['password']
        found_user.otherData = request.form['other_encrypt']
        found_user.otherDataType = request.form['other_type']
        db.session.commit()
        print("Commited an edit for: "+ oldPlatform + " as " + oldTag)

    return redirect(url_for("view"))

@app.route("/add", methods = ["POST"])
def add():
    if 'user' in session:
        platformName = request.form['platform']
        accountTag = request.form['account']
        tagType = request.form['account_type']
        phoneNumber = request.form['phone']
        password = request.form['password']
        otherData = request.form['other_encrypt']
        otherDataType = request.form['other_type']

        entry = PasswordEntries(platformName, accountTag, tagType, phoneNumber, password, otherData, otherDataType)
        db.session.add(entry)
        db.session.commit()
        print("Commited new entry for: "+ entry.accountTag)
        return redirect(url_for("view"))
    else:
        render_template("master_login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('master_login'))

@app.route("/delete", methods = ["POST"])
def delete(entryId):
    return "Placeholder"

if __name__ == "__main__" :
    with app.app_context():
           db.create_all()
    app.run(debug=True)
