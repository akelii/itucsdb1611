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
from classes.education import Education
from classes.operations.education_operations import education_operations
from classes.CV import CV

def personal_cv_page_config(submit_type):
    store = cv_information_operations()
    t = experience_operations()
    now = datetime.now()
    store_CV = cv_operations()
    cvInformations = store.get_cv_information_s()
    experiences = t.get_experience_s()
    cvs = store_CV.get_cvs()
    if submit_type == 'GET':
        return render_template('personal/cv.html',experiences=experiences,cvs=cvs,cvInformations=cvInformations, CurrentCV=0, current_time=now.ctime(),)
    else :

        if request and 'Add_CV' in request.form:
            cvname=request.form['CvName']
            store_CV.add_cv(cvname,now,now)
        elif request and 'newCvName' in request.form and request.method =='POST':
            cvName=request.form['newCvName']
            cvInfo=request.form['newCvInfo']
            store_CV.add_cv(cvName)
            cvs=store_CV.get_cvs()

        return render_template('personal/cv.html', experiences=experiences, cvs=cvs, cvInformations=cvInformations,
                               CurrentCV=0, current_time=now.ctime(), )


def personal_cv_pagewithkey_config(submit_type, key):
    store = cv_information_operations()
    languages = language_operations()
    store_CV = cv_operations()
    t = experience_operations()
    store_experience=experience_operations()
    store_education = education_operations()
    now = datetime.now()
    CurrentCV = store_CV.get_cv(int(key))
    listEducation = store_education.GetEducationListByCVId(key)
    experiences = t.get_experience_s_with_key(key)
    allLanguages = languages.GetAllLanguagesByCVId(key)
    cvs = store_CV.get_cvs()
    updateCV="False"
    if submit_type == 'POST':
        if request and 'deleteLanguage' in request.form and request.method == 'POST':
            deleteIndex = request.form['deleteLanguage']
            languages.DeleteLanguage(deleteIndex)
            allLanguages = languages.GetAllLanguagesByCVId(key)
            updateCV = "TRUE"
        elif request and 'newLanguageName' in request.form and request.method == 'POST':
            newLanguageName = request.form['newLanguageName']
            newLevel = request.form['newLanguageLevel']
            languages.AddLanguage(key, newLanguageName, newLevel)
            allLanguages = languages.GetAllLanguagesByCVId(key)
            updateCV = "TRUE"
        elif request and 'updateLanguageName' in request.form and request.method == 'POST':
            updateName = request.form['updateLanguageName']
            updateLevel = request.form['updateLanguageLevel']
            ID = request.form['updateLanguageId']
            languages.UpdateLanguage(ID, updateName, updateLevel)
            allLanguages = languages.GetAllLanguagesByCVId(key)
            updateCV = "TRUE"
        elif request and 'txtSchoolName' in request.form and request.method == 'POST':
            txtSchoolName = request.form['txtSchoolName']
            txtSchoolDesc = request.form['txtSchoolDesc']
            dpSchoolStart = request.form['dpSchoolStart']
            dpSchoolEnd = request.form['dpSchoolEnd']
            txtGrade = request.form['txtGrade']
            e = Education(None, key, txtSchoolName, txtSchoolDesc, txtGrade, dpSchoolStart, dpSchoolEnd, False)
            store_education.AddEducation(e)
            listEducation = store_education.GetEducationListByCVId(key)
            updateCV = "TRUE"
        elif request and 'deleteEducation' in request.form and request.method == 'POST':
            deleteIndex = request.form['deleteEducation']
            store_education.DeleteEducationWithoutStore(deleteIndex)
            listEducation = store_education.GetEducationListByCVId(key)
            updateCV = "TRUE"
        elif request and 'txtUpdateSchoolName' in request.form and request.method == 'POST':
            txtUpdateSchoolName = request.form['txtUpdateSchoolName']
            txtUpdateSchoolDesc = request.form['txtUpdateSchoolDesc']
            dpUpdateSchoolStart = request.form['dpUpdateSchoolStart']
            dpUpdateSchoolEnd = request.form['dpUpdateSchoolEnd']
            txtUpdateGrade = request.form['txtUpdateGrade']
            id = request.form['hfUpdateEducationId']
            store_education.UpdateEducation(id, txtUpdateSchoolName,txtUpdateSchoolDesc,txtUpdateGrade,dpUpdateSchoolStart,dpUpdateSchoolEnd)
            listEducation = store_education.GetEducationListByCVId(key)
            updateCV = "TRUE"
        elif request and 'newCvName' in request.form and request.method =='POST':
            cvName=request.form['newCvName']
            cvInfo=request.form['newCvInfo']
            store_CV.add_cv_with_key(cvName,key)
            cvs=store_CV.get_cvs()
        elif request and 'DeleteCv' in request.form and request.method =='POST':
            store_CV.delete_cv(key)
            return redirect(url_for('site.personal_cv_page'))
        elif request and 'NewCompanyName' in request.form and request.method=='POST':
            newCompanyName=request.form['NewCompanyName']
            newDescription=request.form['NewDescription']
            newPosition=request.form['NewPosition']
            startDate=request.form['NewStartDate']
            endDate=request.form['NewEndDate']
            store_experience.add_experience(key,newDescription,newCompanyName,newPosition,now,now)
            experiences=store_experience.get_experience_s_with_key(key)
            updateCV = "TRUE"
        elif request and 'DeleteExperience' in request.form and request.method=='POST':
            deleteId=request.form['HiddenId']
            store_experience.delete_experience(deleteId)
            experiences=store_experience.get_experience_s_with_key(key)
            updateCV = "TRUE"
        elif request and 'UpdateExperience' in request.form and request.method=='POST':
            updateId = request.form['HiddenId']
            updatedCompanyName = request.form['UpdatedCompanyName']
            updatedDescription = request.form['UpdatedDescription']
            updatedPosition = request.form['UpdatedPosition']
            updatedStartDate = request.form['UpdatedStartDate']
            updatedEndDate = request.form['UpdatedEndDate']
            store_experience.update_experience(updateId,updatedDescription,now,now,
                                               updatedCompanyName,updatedPosition)
            experiences = store_experience.get_experience_s_with_key(key)
            updateCV = "TRUE"
        elif request.form['add'] == "delete":
            key = request.form['delete_id']
            store.delete_cv_information(key)
        elif request.form['add'] == "update":
            key = request.form['delete_id']
            description = request.form['description']
            store.update_cv_information(key, description, None, None)
        elif request.form['add'] == "delete_experience":
            key = request.form['delete_id']
            t.delete_experience(key)
        elif request.form['add']=="delete_cv":
            key = request.form['delete_id']
            store_CV.delete_cv(key)
        elif request.form['update_ex'] == "update_experience":
            key = request.form['delete_id']
            description = request.form['description']
            experiencepos = request.form['experience_position']
            companyName = request.form['companyName']
            key = request.form['delete_id']
            description = request.form['description']
            t.update_experience(key, description, now, now, companyName, experiencepos)
        elif request and 'Add_CV' in request.form and request.method == 'POST':
            cvname=request.form['CvName']
            store_CV.add_cv(cvname,now,now)
            cvs=store_CV.get_cvs()
        elif request.form['add_ex'] == "add_experience":
            description = request.form['description']
            experience_position = request.form['experience_position']
            companyName = request.form['companyName']
            t.add_experience(CurrentCV[1], description, companyName, experience_position, now, now )
        else:
            description = request.form['description']
            idtype = request.form['add']
            cvinfo = CVInformation(None, '2', description, idtype, None, None)
            store.add_cv_information(cvinfo)
    if updateCV=="TRUE":
        store_CV.update_cv(key)

    return render_template('personal/cv.html', cvs=cvs,CurrentCV=CurrentCV, languages = allLanguages, experiences=experiences, listEducation=listEducation,
                                   current_time=now.ctime())