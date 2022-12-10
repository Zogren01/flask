from flask import Flask, request, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' 
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(80), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author  = db.Column(db.String(80), nullable=False)
    message =  db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    __bind_key__ = 'chat' 

@app.route("/")
def default():
    return redirect(url_for('login_controller'))

@app.route("/login/", methods = ['GET', 'POST'])
def login_controller():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user is not None:
          session['username'] = user.username
          return redirect(url_for("profile", username=username))
        else:
          return 'Invalid username/password'

    return render_template('loginPage.html')

@app.route("/register/", methods = ['GET', 'POST'])
def register_controller():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        retype = request.form['retype']
        email = request.form['email']

        if password == retype:
            try:
                new_user = User(username=username, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("profile", username=username))
            except:
                print("problems with adding to db")
                return "There was an issue adding your profile"
        else:
            return "Passwords do not match"
    else:
        return render_template("register.html")

@app.route("/register/", methods = ['GET', 'POST'])
@app.route("/profile/<username>") 
def profile(username=None): 
    return """
    <!DOCTYPE html>
    <h1>home page stuff </h1>
    <a href="login">login page, change later</a>
    """

@app.route("/logout/") 
def unlogger(): 
    return """
    <!DOCTYPE html>
    <h1>home page stuff </h1>
    <a href="login">login page, change later</a>
    """
@app.route("/new_message/", methods=["POST"]) 
def new_message(): 
    return """
    <!DOCTYPE html>
    <h1>home page stuff </h1>
    <a href="login">login page, change later</a>
    """
@app.route("/messages/") 
def messages(): 
    return """
    <!DOCTYPE html>
    <h1>home page stuff </h1>
    <a href="login">login page, change later</a>
    """
if __name__ == "__main__":
    app.run()