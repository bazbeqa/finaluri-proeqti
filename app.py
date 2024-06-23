from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # შეცვალეთ ეს რეალურ პროექტში
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash('წარმატებით შეხვედით სისტემაში')
            return redirect(url_for('home'))
        else:
            flash('არასწორი მომხმარებლის სახელი ან პაროლი')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('მომხმარებლის სახელი უკვე დაკავებულია')
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('რეგისტრაცია წარმატებით დასრულდა')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('წარმატებით გამოხვედით სისტემიდან')
    return redirect(url_for('login'))

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if 'username' not in session:
        flash('გთხოვთ, ჯერ შეხვიდეთ სისტემაში')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        username = session['username']
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            session.pop('username', None)
            flash('თქვენი ანგარიში წარმატებით წაიშალა')
            return redirect(url_for('home'))
        else:
            flash('მომხმარებელი ვერ მოიძებნა')
    
    return render_template('delete_account.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)