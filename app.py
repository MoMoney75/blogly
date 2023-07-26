"""Blogly application."""
from flask import Flask, redirect,session,render_template,request
from models import db, connect_db, User, Post, create_timestamp

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

###########################
"""home page for app, shows list of all current users"""
@app.route('/', methods=['GET','POST','DELETE'])
def show_all_users():
    """lists all users on home page"""
    list_of_users = User.query.all()
    
    return render_template('home.html', list_of_users=list_of_users)

############################
"""shows existing user details, goes based off of user_id"""
@app.route('/<int:user_id>')
def showUserInfo(user_id):
    user = User.query.get_or_404(user_id)
    
    return render_template('user_info.html', user=user)

############################

"""returns template for creating a new user"""
@app.route('/new_user_form')
def show_new_user_form():

    return render_template('new_user_form.html')

############################
"""gets new user input from form and adds to database"""
@app.route('/new_user_handle', methods=['POST'])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    """creates new instance of User and adds to user table"""
    new_user = User(first_name=first_name, last_name=last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    """returns to home page after submitting"""
    return redirect('/')

##############################


"""EDIT a user, sends user to html form where user can edited/deleted"""
@app.route('/<int:user_id>/edit')
def show_user_edit_form(user_id):
    """show user the edit form"""
    user =  User.query.get_or_404(user_id)
    return render_template('edit_user.html', user = user)

"""edit_user form redirects here after submit"""

##############################
@app.route('/<int:user_id>/edit', methods = ['POST'])
def edit_user(user_id):
     """get the edited form and submit to server"""
     user = User.query.get_or_404(user_id)
     user.first_name = request.form['first_name']
     user.last_name = request.form['last_name']
     user.image_url = request.form['image_url']
         
     db.session.add(user)
     db.session.commit()

     return redirect('/')

############################
"""function for deleting user, gets user id and deletes"""
@app.route('/<int:user_id>/delete',  methods = ['GET','DELETE','POST'])
def delete_user(user_id):
    
    user_id = User.query.get_or_404(user_id)
    db.session.delete(user_id)
    db.session.commit()

    return redirect('/')
0


############################
############################
############################
############################

"""renders template for creating a new post"""
@app.route('/<int:user_id>/create_post')
def showPostForm(user_id):
    userID = User.query.get_or_404(user_id)
    return render_template('createPost.html', userID=user_id)


"""GETS for info for creating new post, creates instance of Post"""
@app.route('/<int:user_id>/new_post', methods = ['GET', 'POST'])
def create_new_post(user_id):
    title = request.form['title']
    content = request.form['content']
    created_at = create_timestamp()
    new_post = Post(title=title, content=content, created_at=created_at,user_id=user_id)

    db.session.add(new_post)
    db.session.commit()   

    return redirect('/')

@app.route('/all_blogs')
def show_all_blogs():
    posts = Post.query.all()
    
    return render_template('all_posts.html', posts=posts)

@app.route('/view_post/<int:post_id>', methods=['GET','POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get
    
    return render_template('view_post.html', post=post)

@app.route('/delete/<int:post_id>', methods=['GET','POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/all_blogs')

@app.route('/edit/<int:post_id>', methods=['GET','POST'])
def show_edit_form(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('edit_form.html', post=post)


@app.route('/edit/<int:post_id>/submit', methods=['GET','POST'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect('/all_blogs')



    

    

    


