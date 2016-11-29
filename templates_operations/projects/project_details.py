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
    store_comments = project_comment_operations()
    if submit_type == 'GET':
        project = store.get_project(key)
        project_comments = store_comments.get_project_comments(key)
        return render_template('projects/project_details.html', project=project, project_comments=project_comments)
    else:
        if 'addComment' in request.form:
            person_id = 2
            commented_project_id = int(key)
            comment = request.form['project_comment']
            project_comment = ProjectComment(None, person_id, commented_project_id, comment)
            store_comments.add_project_comment(project_comment)
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'update' in request.form:
            title = request.form['project_name']
            project_description = request.form['project_description']
            end_date = None
            member_limit = request.form['limit']
            manager = 2
            deleted = '0'
            store.update_project(int(key), title, project_description, end_date, member_limit, manager, deleted)
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'delete' in request.form:
            comment_key = request.form['delete']
            store_comments.delete_project_comment(int(comment_key))
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'edit' in request.form:
            comment_key = request.form['edit']
            new_comment = request.form['newComment']
            store_comments.update_project_comment(comment_key, new_comment, False)
            return redirect(url_for('site.projects_details_page', key=key))





