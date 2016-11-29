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

def project_comments_page_config(submit_type, key):
    store = project_operations()
    store_comments = project_comment_operations()

    if submit_type == 'GET':
        project_comments = store_comments.get_project_comments(key)
        return render_template('projects/project_comments.html', project_comments=project_comments)
    elif 'delete' in request.form and submit_type == 'POST':
        comment_key = request.form['delete']
        store_comments.delete_project_comment(int(comment_key))
        return render_template('dashboard.html')
    elif 'edit' in request.form and submit_type == 'POST':
        comment_key = request.form['edit']
        new_comment = request.form['newComment']
        store_comments.update_project_comment(comment_key, new_comment, False)
        return render_template('dashboard.html')



