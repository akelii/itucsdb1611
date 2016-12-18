from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from flask_login import current_user, login_required
from datetime import datetime
from classes.operations.project_operations import project_operations
from classes.operations.person_operations import person_operations
from classes.project import Project
from classes.look_up_tables import *
from templates_operations.user import*


def project_create_page_config(submit_type):
    if submit_type == 'GET':
        listProjectType = GetProjectType()
        listProjectThesisType = GetProjectThesisType()
        listDepartment = GetDepartment()
        listProjectStatusType = GetProjectStatusType()
        listManager = GetManagerList()
        return render_template('projects/create_project.html', listProjectType=listProjectType, listProjectThesisType=listProjectThesisType, listDepartment=listDepartment, listProjectStatusType=listProjectStatusType, listManager=listManager)
    else:
        if 'Add' in request.form.values():
            store = project_operations()
            title = request.form['project_name']
            project_description = request.form['project_description']
            project_type = request.form['project_type']
            project_thesis_type = request.form['project_thesis_type']
            department = request.form['department']
            start_date = request.form['start']
            #start_date = None
            end_date = request.form['end_date']
            if end_date > str(datetime.datetime.now()):#ileri tarihte bitecekse
                project_status_type = 2
            else:#süre bitmişse
                project_status_type = 3
            member_limit = request.form['limit']
            created_by = person_operations.GetPerson(current_user, current_user.email)[0]#current_user proje oluşturuyor
            manager = request.form['project_manager']
            project = Project(None, title, project_description, project_type, project_thesis_type, department,
                              project_status_type, start_date, end_date, member_limit, None, created_by, manager)
            store.add_project(project)
            return redirect(url_for('site.home_page'))