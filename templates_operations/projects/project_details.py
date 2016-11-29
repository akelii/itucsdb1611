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
   






