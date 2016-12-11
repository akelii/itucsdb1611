from flask import render_template
import os
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from classes.operations.person_operations import person_operations
from classes.look_up_tables import *
from classes.person import Person
from werkzeug.utils import secure_filename
from passlib.apps import custom_app_context as pwd_context
from templates_operations.user import*

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def register_page_config(request):
    if request.method == 'GET':
        listTitle = GetTitleList()
        listAccount = GetAccountTypeList()
        return render_template('register.html', listTitle=listTitle, listAccount=listAccount)
    else:
        if 'register' in request.form:
            store = person_operations()
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            eMail = request.form['eMail']
            pswd = pwd_context.encrypt(request.form['pswd'])
            accountType = request.form['account']
            title = request.form['title']
            file = request.files['file']
            gender = request.form['r1']
            if gender == 'male':
                gender = False
            elif gender == 'female':
                gender = True
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/user_images', filename))
            else:
                if gender == 'male':
                    filename = 'noimage_male.jpg'
                else:
                    filename = 'noimage_female.jpg'
            p = Person(None, first_name, last_name, accountType, eMail, pswd, gender, title, filename, False)
            u = User(eMail, pswd)
            store.AddPerson(p)
            AddUser(u)
            return redirect(url_for('site.home_page'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS