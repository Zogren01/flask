from flask import Flask, request, url_for, redirect, render_template, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json

app = Flask(__name__)
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
          return render_template('loginPage.html') + '<p class="err">Invalid username/password</p>'

    return render_template('loginPage.html')

@app.route("/register/", methods = ['GET', 'POST'])
def register_controller():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        retype = request.form['retype']
        
        if password == retype:
            try:
                new_user = User(username=username, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("profile", username=username))
            except:
                return render_template("register.html") + '<p class="err">There was an issue adding your profile</p>'
        else:
            return render_template("register.html") + '<p class="err">Entered passwords do not match</p>' 

    return render_template("register.html")

@app.route("/profile/<username>", methods = ['GET', 'POST'])
def profile(username=None): 
    if "username" in session:
        messages = Message.query.order_by(Message.date_created.desc()).all()
        user = User.query.filter_by(username=username).first()
        return render_template('chat_page.html', user=user, messages=messages)
    else:
        return redirect(url_for("login_controller"))

@app.route("/logout/") 
def unlogger(): 

    session.clear()
    return render_template("logoutPage.html")
	
@app.route("/new_message/", methods=["POST"]) 
def new_message(): 
    message = request.form.get('message')
    author = request.form.get('author') 
    new_chat = Message(author=author, message=message)
    try:
        db.session.add(new_chat)
        db.session.commit()
        addChat = {'author': author, 'message': message}
        return json.dumps(addChat)
    except Exception as e:
        print("There was an error adding your chat message")

@app.route("/messages/")  
def messages(): 
    all_chats = Message.query.order_by(Message.date_created.desc()).all()
    all_chats_json = { }
    for index, element in enumerate(all_chats):
        all_chats_json[index] = { }
        all_chats_json[index]['author'] = element.author
        all_chats_json[index]['message'] = element.message
        all_chats_json[index]['datetime'] = element.date_created.date()
    return jsonify(all_chats_json)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run()