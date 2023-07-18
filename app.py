"""Blogly application."""

from flask import Flask, redirect,session,render_template,request
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()
app.debug = True
app.config['SECRET_KEY'] = 'SEKRET'


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/', methods=['GET','POST','DELETE'])
def show_all_users():
    """lists all users on home page"""
    list_of_users = User.query.all()

    return render_template('home.html', list_of_users=list_of_users)

@app.route('/new_user', methods=['POST'])
def create_user():
    """gets new user input from form and adds to database"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

@app.route('/<int:userID>/delete',  methods = ['GET','DELETE','POST'])
def delete_user(userID):
    """function for deleting user"""

    userID = User.query.get_or_404(userID)
    db.session.delete(userID)
    db.session.commit()

    return redirect('/')

@app.route('/<int:userID>/edit')
def show_edit_form(userID):
    """show user the edit form"""
    user =  User.query.get_or_404(userID)
    return render_template('edit_user.html', user = user)



@app.route('/<int:userID>/edit', methods = ['POST'])
def edit_user(userID):
     """get the edited form and submit to server"""
     user = User.query.get_or_404(userID)
     user.first_name = request.form['first_name']
     user.last_name = request.form['last_name']
     user.image_url = request.form['image_url']
         
     db.session.add(user)
     db.session.commit()

     return redirect('/')


@app.route('/<int:user_id>')
def showUserInfo(user_id):
    """shows existing user details, goes based off of user_id"""
    userID = User.query.get_or_404(user_id)
    
    return render_template('user.html', userID = userID)


