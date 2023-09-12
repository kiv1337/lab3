from flask import Flask, request, render_template, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/delta/OneDrive/Рабочий стол/Учёба 407/Кочетков/lab3/database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    username = db.Column(db.String(100), unique=True, primary_key=True)
    password = db.Column(db.String(100))
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def check_password(self, password):
        return self.password == password

with app.app_context():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Пользователь с таким именем уже существует."
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        new_user = User(username=username, password=hashed_password.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        return redirect('/main')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/main')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['username'] = user.username
            return redirect('/main')

    return render_template('login.html')


@app.route('/main')
def main():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        return render_template('main.html', user=user)
    
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/')
def index():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
