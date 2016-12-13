from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from datetime import datetime
from classes.operations.project_operations import project_operations

from classes.project import Project


def project_search_page_config(submit_type):
    store = project_operations()
    if submit_type == 'GET':
        projects = store.get_projects()
        return render_template('projects/search_project.html', projects=projects)
    else:
        if 'check' and 'details' in request.form:
            key = request.form['check']
            return redirect(url_for('site.projects_details_page', key=key))

