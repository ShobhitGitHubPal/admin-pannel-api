############### this code is create for login, logout and forgot using json file update in json file ###############
'''from flask import Flask, render_template, request, url_for, redirect, session, json
# from flask_login import logout_user
# from flask_login import LoginManager, UserMixin

import pymongo
from pymongo import MongoClient
from mongoengine import connect, StringField, IntField
from flask_cors import CORS
# client = MongoClient()

with open('config.json', 'r') as c:
     params= json.load(c) ["params"]


# ...

app = Flask(__name__)

# connect('mdbase')
app.config['SECRET_KEY'] = 'the random string'

# client=MongoClient('mongodb://localhost:27017/')
# app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
# client = pymongo.MongoClient('localhost',27017)
# db=client['mydb']
# collection = db['login']
# mongo=PyMongo(app)

@app.route('/login', methods=('GET', 'POST'))
def login():
    if 'user' in session and session['user'] == params['username']:
        return render_template('index.html', params= params)
    if request.method == "POST":
        username= request.form.get('username')
        password= request.form.get('password')
 
        if (username == params['username'] and (password== params['password'])):
            session['user'] = username
            
            return render_template('index.html',params=params)
        else:
            return 'please check your email or password'
        
    return render_template('login.html')


@app.route('/logout/')
def logout():
    print('loging out...')
    session.pop('user', None)
    return redirect('/login')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        
        username= request.form.get('username')
        new_password = request.form.get('new_password')
        print ('mlkkhtyrtxfdxdszfd::::::',username, new_password)
        if username == params['username'] :
            params['password'] = new_password
            with open('config.json', 'w') as c:
                json.dump({'params': params}, c)
            return 'Password updated successfully!'
        else:
            return 'your email is not match'
    return render_template('forgot.html')

if __name__== ('__main__'):
    app.run(debug=True,port=2020)
 '''
#######################################################################################################################


from flask import Flask, render_template, request, url_for, redirect, session, json, flash, jsonify, send_from_directory
from flask_login import logout_user
from flask_pymongo import PyMongo
from pymongo import MongoClient
from mongoengine import connect, StringField, IntField
import os
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from functools import wraps
# from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
# import base64
# from flask_bootstrap import Bootstrap
# import cloudinary
# import cloudinary.uploader
app = Flask(__name__, static_folder='static')
# Bootstrap(app)
img = os.path.join('static', 'image')
UPLOAD_FOLDER = 'image'


app.config['UPLOAD_FOLDER'] = "static/image"
app.config['SECRET_KEY'] = 'the random string'


app.config['MONGO_URI'] = 'mongodb://localhost:27017/admin_dashboard'
app.config["UPLOAD_FOLDER"] = "static/uploads/"
mongo = PyMongo(app)
client = MongoClient(app.config['MONGO_URI'])
db = client.get_database()
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])
# db = client['admin_dashboard']
admin_collection = db['admins']
admin_collection = db['images']
posts_collection = db['posts']
print(posts_collection)

# Initialize LoginManager
login_manager = LoginManager(app)

# User class
class User(UserMixin):
    def __init__(self, id, is_active=True):
        self.id = id
        # self.is_active = is_active
        def is_active(self):
        # Add your logic here to determine if the user is active
            return True  # Replace with your actual logic
################  this code use for insert username and password in database###################
# Check if admin credentials exist
# if not admin_collection.find_one():
#     admin_username = 'palshobhit@gmail.com'
#     admin_password = '336377'
#     admin_collection.insert_one({'username': admin_username, 'password': admin_password})
#################################################################################################

#################### use for insert pic in database#######################
# if not admin_collection.find_one():
#     image="PAL.jpg"
#     admin_collection.insert_one({'image':image})

################################################


######################## for login###################################

# User loader function
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Login configuration
login_manager.login_view = 'login'


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if 'user' in session and session['user'] == admin_username:
    #     return render_template('index.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match
        admin = mongo.db.admins.find_one(
            {'username': username, 'password': password})
        print(f'jhjcjgu{admin}')
        if admin:
            
            user = User(admin['_id'])
        
            login_user(user)

            # return render_template('index.html')
            return jsonify({'message':'you have been successfully login'})######render_template('index.html')
        else:
            return jsonify({'message': 'Invalid username or password!'})
    return jsonify({'message': 'yes'})
    # return render_template('login.html')
  #############################################################################################

############################ for logout ###################################################################

@app.route('/logout/')
@login_required 
def logout():
    logout_user()  # Log out the current user
    return jsonify({'message': 'You have been successfully logged out'})


# def logout():
#     # if 'admin' in session:
#     print('loging out...')
#     session.pop('admin', None)
#     return jsonify({'message':'you are successfully logout'})
#     # return redirect('/login')
#########################################################################################################

################## for forgot #############################################


@app.route('/forgot/', methods=['GET', 'POST'])
@login_required
def forgot():
    # if 'admin' in session:
    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        print('mlkkhtyrtxfdxdszfd::::::', username, new_password)
        admin = mongo.db.admins.find_one({'username': username})
        print(admin)
        if admin:
        
            # '_id':
            mongo.db.admins.update_one({'_id': admin['_id']}, {
                                       '$set': {'password': new_password}})

            # admin_password = new_password
            # new_password.update(admin_password)
            # with open('config.json', 'w') as c:
            #     json.dump({'params': params}, c)
            return jsonify({'message':'Password updated successfully!'})
            # return 'Password updated successfully!'
        else:
            return jsonify({ 'message':'your email is not match'})
            # return "your email is not match"
    return jsonify({'message': 'yes'})
    # return render_template('forgot.html')
##########################################################################
############################ this code is use for upload image in file as image name #############################


@app.route('/upload_image', methods=['GET', 'POST'])
@login_required
def upload():
    # if 'admin' in session:
    if request.method == 'POST':
        f = request.files['file']     # f.save(os.path.join())
        print(f)
        # filename = secure_filename(f.filename)
        filename = f.filename
        f.save('static/image/' + filename)
        # f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # f.save('static/image/'+f.filename)
        # image_data= f.read()# Read the image data
        image_doc = {
            'filename': f.filename
            # 'data': image_data
        }
        db['images'].insert_one(image_doc)
        return jsonify({'message':'successfully upload'})
        # f.save('static/image/'+f.filename)
        # return redirect('/web.html?filename=' + filename)

    # return render_template('upload_image.html')
    return jsonify({'message':'yes'})

################################################################################################


############################# update image########################################
@app.route('/update_image', methods=['POST', 'GET'])
@login_required
def update_image():
    # if 'admin' in session:
    if request.method == 'POST':
        img = request.files['img']
        print('ljwkdqub', img.filename)
        img.save('static/image/' + img.filename)
        image = mongo.db.images.find_one({'filename': img.filename})
        if image:
            return jsonify({'message': 'successfully update'})
            # return render_template('web.html', image=image)
        else:
            return 'Image does not exist'
    return jsonify({'message': 'yes'})
    # return render_template('update_image.html')
###################################################################################################


#################### here gallery show all images ########################################################
@app.route('/gallery_image')
@login_required
def gallery_image():
    # if 'admin' in session:
    image_dir = os.path.join(app.static_folder, 'image')
    image_files = os.listdir(
        "C:\\Users\\hp pc\\OneDrive\\Desktop\\admpnl\\static\\image\\")
    image_dir = os.path.join(app.static_folder, 'image')
    image_files = os.listdir(
        "C:\\Users\\hp pc\\OneDrive\\Desktop\\admpnl\\static\\image")
    image_data = []
    for images in image_files:
        # Example: Retrieve additional data for each image
        image_path = os.path.join(image_dir, images)
        image_size = os.path.getsize(image_path)
        # , 'size': image_size
        image_data.append({'filename': images, 'size': image_size})
        print(image_data)
    # file_data = mongo.db.images.find_one({'filename': image})
    # if file_data:
    #     return send_file(file_data['C:\\Users\\hp pc\\OneDrive\\Desktop\\admpnl\\static\\image'], mimetype='image/')  # Adjust mimetype based on your image file type
    # else:
    #     return 'Image not found'
    # image_files = os.listdir('static/images')
    return jsonify({'message': 'yes show gallery'})
    # return render_template('gallery_image.html',image_files=image_files )  ###     image_files=image_files
###################################################################################################################

# Check if admin credentials exist
# if not admin_collection.find_one():
#     title = 'palshobhit@gmail.com'
#     admin_password = '336377'
#     desc='kneneiueuveivbehvejlvnekje'
#     posts_collection.insert_one({'title1': admin_username, 'title2': admin_password,'description':desc})

###################### here show title ##############################


@app.route('/show_title', methods=['GET'])
@login_required
def show():
    document = posts_collection.find_one()
    print(document)
    # title1 = document.get('title1', '') 
    return jsonify({'messageb': ' show all title',
                    "title1": title1,
                    # "title2": title2,
                    # "description": document.description
                    })
    # return render_template('show.html',document=document)
################################################
#
# ########## for update title #######################################


@app.route('/update_title', methods=['GET', 'POST'])

def update():
    # _id = request.form.get('_id')
    new_title1 = request.form.get('title1')
    new_title2 = request.form.get('title2')
    new_description = request.form.get('description')
    print(new_title1, new_title2, new_description)

    collection = client.admin_dashboard.posts
    collection.update_one({}, {'$set': {'title1': new_title1,
                                        "title2": new_title2,
                                        "description": new_description
                                        }})
    return jsonify({'message': 'update title'})
    # return render_template('update_title.html')
######################################################################################################

############## these code is use for insert data in database ###########################################
    # new_document={
    #     "title1": new_title1,
    #     "title2":new_title2,
    #     "description":new_description
    # }
    # collection.insert_one(new_document)
    # print("document::",new_document)
############################################################################################################


################## this code is user for update image from directly database ###########################################
# @app.route('/update', methods=['GET','POST'])
# def edit():
#     if request.method=='POST':
#         new_image = request.files['file']
#         if new_image:
#             image_data =new_image.read()
#             admin_collection.update_one({} ,{'$set': {'image': image_data}})   #{'_id': admin['_id']},
#             return 'update image succesfully'

#     return render_template('update.html' )

# @app.route('/show')
# def display_image():
#     document = admin_collection.find_one({})
#     if document and 'image' in document:
#         image_data = document['image']
#         image_base64 = base64.b64encode(image_data).decode('utf-8')
#         return render_template('show.html', image_data=image_base64)
#     return 'Image not found'
##############################################################################################################


if __name__ == ('__main__'):
    app.run(debug=True)
