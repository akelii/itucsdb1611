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

def project_add_comments_page_config(submit_type, key):
    store_comments = project_comment_operations()
    if submit_type == 'GET':
        return render_template('projects/project_comment_add.html')
    elif 'add' in request.form and submit_type == 'POST':
        person_id = 2
        commented_project_id = int(key)
        comment = request.form['project_comment']
        project_comment = ProjectComment(None, person_id, commented_project_id, comment)
        store_comments.add_project_comment(project_comment)
    return render_template('dashboard.html')

