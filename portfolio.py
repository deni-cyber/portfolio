from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from models import Project,Message,Testimony,Blog,Art
import random

import os
from werkzeug.utils import secure_filename

#here we define other required variables
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


#app configuration
app = Flask(__name__)
#the app setttings go here.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'this_string_is_sacred'


#here other requred functions are defined.
#########
#########
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


##########
##########
#url routing starts here 

@app.route("/")
def home ():
    projects_list=Project.get_from_db()
    if len(projects_list)>3:
        projects_list=random.sample(projects_list,4)

    else:
        projects_list=projects_list

    testimony_list=Testimony.get_from_db()
    return render_template('landingpage.html', projects_list=projects_list, testimony_list=testimony_list)

@app.route("/uploaded_file/<filename>/")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/admin/', methods=["POST","GET"])
def admin ():
    art_category_list=['Digital','Posta', 'logo', 'drawing', 'painting', ]
    projects_list=Project.get_from_db()
    messages_list=Message.get_from_db()
    testimony_list=Testimony.get_from_db()
    blog_list=Blog.get_from_db()
    art_list=Art.get_from_db()
    if not projects_list :
        flash('no projects to show')
    if not messages_list:
        flash('no messages to show')
    if not testimony_list:
        flash ('no comments to show')
    if not blog_list:
        flash ('no blogs to show')
    if not art_list:
        flash ('no art to show')
    return render_template('admin.html', projects_list=projects_list,messages_list=messages_list,testimony_list=testimony_list, 
                           blog_list=blog_list, art_category_list=art_category_list, art_list=art_list)


@app.route('/add_project/',methods=['POST', 'GET'])
def add_project():
    if request.method =="POST":
        if not request.form['name'] or not request.form['client'] or not request.form['description']:
            flash('Please enter all the fields', 'error')

        else:

            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)  

                name=(request.form['name'])
                client=(request.form['client'])
                description=(request.form['description'])
                project_image_url=url_for('uploaded_file', filename=filename)
                project_image_filename=filename

                project=Project(name, client, description ,project_image_url,project_image_filename)
                project.save_to_db()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   
                flash(f'Project-{project} added to the Projects successfuly')
                return redirect(request.url)
            else:
                flash('ivalid image file')
                return redirect(request.url)
        return redirect(url_for('admin'))
    else:
        # Redirect GET requests to admin page
        return redirect(url_for('admin'))

@app.route('/add_art/',methods=['POST', 'GET'])
def add_art():
    if request.method =="POST":
        if not request.form['name'] or not request.form['category'] or not request.form['description']:
            flash('Please enter all the fields', 'error')

        else:

            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)  

                name=(request.form['name'])
                category=(request.form['category'])
                description=(request.form['description'])
                art_image_url=url_for('uploaded_file', filename=filename)
                art_image_filename=filename

                art=Art(name, category, description ,art_image_url,art_image_filename)
                art.save_to_db()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))   
                flash(f'Art-{art} added to the Arts & Graphics successfuly')
                return redirect(request.url)
            else:
                flash('ivalid image file')
                return redirect(request.url)
        return redirect(url_for('admin'))
    else:
        # Redirect GET requests to admin page
        return redirect(url_for('admin'))

@app.route('/modify/', methods=["POST", "GET"])
def modify():
    if request.method == 'POST':
        # Get the 'project' value from the form
        project = request.form.get('project')

        if not project:
            flash('No project has been selected')
            return redirect(url_for('admin'))

        # Split the 'project' value assuming it's formatted as "<project_id> <filename>"
        try:
            project_parts = project.split()
            if len(project_parts) >= 2:
                project_id, filename = project_parts[0], project_parts[1]

                # Remove the file associated with the project
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(file_path):
                    os.remove(file_path)

                # Remove project from the database
                Project.remove_from_db(project_id)

                flash('Project deleted successfully')
            else:
                flash('Invalid project selection format')

        except FileNotFoundError:
            flash(f'File not found: {filename}')
        except Exception as e:
            flash(f'An error occurred: {str(e)}')

        return redirect(url_for('admin'))

    else:
        # Redirect GET requests to admin page
        return redirect(url_for('admin'))

@app.route('/amodify_art/', methods=["POST", "GET"])
def modify_art():
    if request.method == 'POST':
        # Get the 'project' value from the form
        art = request.form.get('art')

        if not art:
            flash('No project has been selected')
            return redirect(url_for('admin'))

        # Split the 'project' value assuming it's formatted as "<project_id> <filename>"
        try:
            art_parts = art.split()
            if len(art_parts) >= 2:
                art_id, filename = art_parts[0], art_parts[1]

                # Remove the file associated with the project
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(file_path):
                    os.remove(file_path)

                # Remove project from the database
                Art.remove_from_db(art_id)

                flash('Art deleted successfully')
            else:
                flash('Invalid project selection format')

        except FileNotFoundError:
            flash(f'File not found: {filename}')
        except Exception as e:
            flash(f'An error occurred: {str(e)}')

        return redirect(url_for('admin'))

    else:
        # Redirect GET requests to admin page
        return redirect(url_for('admin'))



@app.route('/message/', methods=["POST"])
def message ():
    if request.method == "POST":
        if not request.form['username'] or not request.form['useremail'] or not request.form['message'] :
            flash('Please fill in all the fields', 'error')

        else:
            username=request.form['username']
            useremail=request.form['useremail']
            subject=request.form['subject']
            message=request.form['message']
            message_part=Message(username,useremail,subject,message)
            message_part.add_to_db()
            flash(f'message has been sent, thanks for contacting Denis.')
        return redirect(url_for('contacts'))

@app.route('/delete_message/', methods=['post','get'])
def delete_message():
    if request.method == "POST":
        message_id = request.form.get('message_id')

        if not message_id:  
            flash('No message has been selected', 'error')
        else:
            if Message.delete_message(message_id):
                flash('Message deleted successfully', 'success')
            else:
                flash('Failed to delete the message', 'error')

        return redirect(url_for('admin')) 
    
@app.route('/testimony/', methods=['post','get'])
def testimony ():
    if request.method == "POST":
        if not request.form['name'] or not request.form['message'] :
            flash('Please enter all the fields', 'error')

        else:
            name=request.form['name']
            message=request.form['message']
            print(name)
            print(message)
            testimony_part=Testimony(name, message)
            testimony_part.add_to_db()
            flash(f'comment has been sent, thank you for sharing.')
        return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/delete_testimony/', methods=['post', 'get'])
def delete_testimony():
    if request.method == "POST":
        testimony_id = request.form.get('testimony_id')

        if not testimony_id:  
            flash('No message has been selected', 'error')
        else:
            Testimony.delete_message(testimony_id)
            flash('Testimony deleted successfully', 'success')

        return redirect(url_for('admin')) 

@app.route('/projects/')
def projects ():
    projects_list=Project.get_from_db()
    if not projects_list:
        flash('no projects available')
    return render_template('projects.html', projects_list=projects_list)


@app.route('/contacts/')
def contacts ():
    return render_template('contacts.html')


@app.route('/about/')
def about ():
    return render_template('about.html')

@app.route('/blog/', methods=['post', 'get'])
def blog():
    blog_list=Blog.get_from_db()
    blog_list.reverse()
    return render_template('blogs.html', blog_list=blog_list)

@app.route('/art/')
def art ():
    art_list=Art.get_from_db()
    if not art_list:
        flash('no art available')
    return render_template('art.html', art_list=art_list)

@app.route('/add-blog/' , methods=['POST', 'GET'])
def add_blog():
    if request.method =='POST':
        if not request.form['title'] or not request.form['outhor'] or not request.form['description']:
            flash('fill in all the areas')
        else:
            try:
                blog=request.form
                blog_to_save=Blog(blog['title'], blog['outhor'], blog['description'])
                blog_to_save.save_to_db()
                flash('blog posted succesfully')
            except:
                flash('an error occured')
            return render_template('admin.html')
    return render_template('admin.html')
@app.route('/delet_blog/' , methods=['POST', 'GET'])
def delete_blog():
    if request.method == "POST":
        blog_id = request.form.get('blog_id')
        if not blog_id:  
            flash('No blog has been selected', 'error')
        else:
            Blog.remove_from_db(blog_id)
            flash('Blog deleted successfully', 'success')
        return redirect(url_for('admin')) 

if __name__ =='__main__':
    app.run(debug=True)