from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/finance'  # Update with your DB credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Defining Models based on the provided tables

class User(db.Model):
    __tablename__ = 'User'
    User_Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Income = db.Column(db.Numeric(10, 2))
    Location = db.Column(db.String(100))
    Password = db.Column(db.String(255), nullable=False)

class Asset(db.Model):
    __tablename__ = 'Asset'
    Asset_Id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String(50), nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Stock = db.Column(db.Integer, default=0)
    Banks = db.Column(db.String(100))
    Total_Value = db.Column(db.Numeric(15, 2))
    Purchase_Price = db.Column(db.Numeric(15, 2))
    Real_Estate_Value = db.Column(db.Numeric(15, 2))

class Portfolio(db.Model):
    __tablename__ = 'Portfolio'
    Portfolio_Id = db.Column(db.Integer, primary_key=True)
    Password = db.Column(db.String(255), nullable=False)
    User_Id = db.Column(db.Integer, db.ForeignKey('User.User_Id'))
    Asset_Id = db.Column(db.Integer, db.ForeignKey('Asset.Asset_Id'))
    Creation_Date = db.Column(db.Date, nullable=False)
    user = db.relationship('User', backref=db.backref('portfolios'))
    asset = db.relationship('Asset', backref=db.backref('portfolios'))

# Routes for displaying information and forms

@app.route('/')
def index():
    users = User.query.all()  # Fetch all users
    return render_template('index.html', users=users)

@app.route('/user/<int:user_id>')
def user_details(user_id):
    user = User.query.get(user_id)
    portfolios = Portfolio.query.filter_by(User_Id=user_id).all()
    return render_template('user_details.html', user=user, portfolios=portfolios)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        income = request.form['income']
        location = request.form['location']
        password = request.form['password']
        
        new_user = User(Name=name, Age=age, Email=email, Income=income, Location=location, Password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_user.html')

# Initialize the app
if __name__ == '__main__':
    db.create_all()  # Ensure that all tables are created
    app.run(debug=True)
