from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from datetime import datetime
from datetime import datetime
from classes.operations.project_operations import project_operations
from classes.project import Project
from classes.model_config import dsn
import psycopg2 as dbapi2


def project_update_page_config(submit_type, key):
    store = project_operations()
    if submit_type == 'GET':
        project = store.get_project(key)
        #return redirect(url_for('site.projects_update_page'), key=key)
        return render_template('projects/project_update.html', project=project)
    elif request and 'submit' in request.form and request.method == 'POST':
        title = request.form['project_name']
        project_description = request.form['project_description']
        end_date = None
        member_limit = request.form['limit']
        manager = 2
        deleted = '0'
        store.update_project(int(key), title, project_description, end_date, member_limit, manager, deleted)
        return render_template('dashboard.html')
