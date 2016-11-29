from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
import time
from classes.operations.CV_operations import cv_operations
from classes.operations.CVInformation_operations import cv_information_operations
from classes.CVInformation import CVInformation
from classes.Experience import Experience
from classes.operations.Experience_operations import experience_operations
from classes.operations.language_operations import language_operations

def personal_cv_page_config(submit_type):
    store = cv_information_operations()
    languages=language_operations()
    t = experience_operations()
    now = datetime.now()
    if submit_type == 'GET':
        cvInformations=store.get_cv_information_s()
        experiences=t.get_experience_s()
        allLanguages = languages.GetAllLanguagesByCVId('0')
        return render_template('personal/cv.html',cvInformations=cvInformations, languages = allLanguages, experiences=experiences,current_time=now.ctime(),)
    else:
        if request and 'deleteLanguage' in request.form and request.method=='POST':
            deleteIndex = request.form['deleteLanguage']
            languages.DeleteLanguage(deleteIndex)
            allLanguages = languages.GetAllLanguagesByCVId('1')
            return render_template('personal/cv.html', languages=allLanguages)


        elif request.form['add']=="delete":
            key =request.form['delete_id']
            store.delete_cv_information(key)
        elif request.form['add']=="update":
            key = request.form['delete_id']
            description = request.form['description']
            store.update_cv_information(key, description, None,None)
        elif request.form['add']=="delete_experience":
            key =request.form['delete_id']
            t.delete_experience(key)
        elif request.form['update_ex'] == "update_experience":
            key = request.form['delete_id']
            description = request.form['description']
            experiencepos = request.form['experience_position']
            companyName = request.form['companyName']
            key = request.form['delete_id']
            description = request.form['description']
            t.update_experience(key, description, now, now,companyName,experiencepos)

        elif  request.form['add_ex']=="add_experience":
            description=request.form['description']
            experience_position=request.form['experience_position']
            companyName=request.form['companyName']
            experience=Experience(None,'2',description,companyName,None,None,experience_position)
            t.add_experience(experience)

        else:
            description=request.form['description']
            idtype=request.form['add']
            cvinfo=CVInformation(None,'2',description,idtype,None,None)
            store.add_cv_information(cvinfo)
        return redirect(url_for('site.personal_cv_page'))
