from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from datetime import datetime
from classes.operations.project_operations import project_operations
from classes.project import Project

def project_create_page_config(submit_type):
    if submit_type=='GET':
        return render_template('projects/create_project.html')
    else:
        if 'Add' in request.form.values():
            store = project_operations()
            title = request.form['project_name']
            project_description = request.form['project_description']
            project_type = 1
            project_thesis_type = None
            department = 1
            project_status_type = 1
            start_date = datetime.now()
            end_date = None
            member_limit = 4
            created_by = 2
            manager = 2
            project = Project(None, title, project_description, project_type, project_thesis_type, department,
                              project_status_type, start_date, end_date, member_limit, None, created_by, manager)
            store.add_project(project)
            return render_template('dashboard.html')