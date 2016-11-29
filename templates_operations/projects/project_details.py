from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from datetime import datetime
from datetime import datetime
from classes.project_comment import ProjectComment
from classes.operations.project_operations import project_operations
from classes.operations.project_comment_operations import project_comment_operations
from classes.project import Project
from classes.model_config import dsn
import psycopg2 as dbapi2

def project_details_page_config(submit_type, key):
    store = project_operations()
    store_comment = project_comment_operations()
    if submit_type == 'GET':
        project = store.get_project(key)
        project_comments = store_comment.get_project_comments(key)
        return render_template('projects/project_details.html', project=project, project_comments=project_comments)
    else:
       # if request and 'update' in request.form and request.method == 'POST':
       #     project = store.get_project(key)
       #     return redirect(url_for('site.projects_update_page'), key=key)
            #return render_template('projects/project_update.html',  project=project)
            #return render_template('dashboard.html')
        if request and 'add' in request.form and request.method == 'POST':
            person_id = 2
            project_id = key
            comment = request.form['project_comment']
            create_date = datetime.datetime.now()
            update_date = None
            project_comment = ProjectComment(None, person_id, project_id, comment, create_date, update_date)
            store_comment.add_project_comment(project_comment)
            return redirect(url_for('site.projects_detail_page', key=key))







