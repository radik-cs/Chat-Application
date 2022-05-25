
from email import message
import json
import hashlib
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy.exc import IntegrityError




app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return "<User %>" % self.username
 
class Chat(db.Model):
    __bind_key__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(200), nullable=False)

logged_in_users = [];

@app.route('/')
def default():
    if 'username' not in session:
        return redirect(url_for('login_controller'))

    return redirect(url_for('profile', username=session['username']))

@app.route('/register', methods=['GET', 'POST'])
def register_controller():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']


        if password != cpassword:
            print("Passwords not equal")
            return redirect(url_for('register_controller'))

        try:
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            print("Username or email already exists")
            return redirect(url_for('register_controller'))

        return redirect(url_for('login_controller'))
   
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_controller():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(username, password)

        user = User.query.filter_by(username=username, password=password).first()
        if user is None:
            print('User not found')
            return redirect('/login')
        else:
            logged_in_users.append(user)
            session["loggedin"] = True
            session["username"] = username
            return redirect(url_for('profile', username=username))

    return render_template('login.html')

@app.route('/profile/<username>')
def profile(username=None):
    return render_template('profile.html', username=username)

@app.route('/logout')
def unlogger():
    session.pop('username', None)
    return redirect(url_for('login_controller'))

@app.route('/new_message', methods=['POST'])
def new_message():
    message = request.form.get("message")
    sender = request.form.get("username")

    print(message)
    print(sender)


    try:
        new_message = Chat(sender=sender, message=message)
        db.session.add(new_message)
        db.session.commit()

    except Exception as e:
        print(str(e))

    return jsonify(sender=sender, message=message)
    


@app.route('/messages')
def messages():
    username = session.get('username')
    chat = Chat.query.all()

    messages = []
    for c in chat:
        messages.append({"id": c.id, "author": c.sender, "message": c.message})

    return jsonify(messages=messages)

if __name__ == '__main__':
    app.run(debug=True)