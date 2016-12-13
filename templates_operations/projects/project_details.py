from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask_login import current_user
from datetime import datetime
from datetime import datetime
from classes.project_comment import ProjectComment
from classes.operations.project_operations import project_operations
from classes.operations.project_comment_operations import project_comment_operations
from classes.operations.person_operations import person_operations
from classes.project import Project
from classes.operations.work_log_operations import work_log_operations
from classes.look_up_tables import *
from classes.model_config import dsn
import psycopg2 as dbapi2

def project_details_page_config(submit_type, key):
    store = project_operations()
    store_comments = project_comment_operations()
    store_worklogs = work_log_operations()
    if submit_type == 'GET':
        project = store.get_project(key)
        listManager = GetManagerList()
        project_comments = store_comments.get_project_comments(key)
        worklogs = store_worklogs.GetWorkLogByProjectId(key)
        current_user_objectid = person_operations.GetPerson(current_user, current_user.email)[0]#current_userın person tablosundaki halinin objectidsi
        project_creator = project[8]#projeyi oluşturan kişi
        return render_template('projects/project_details.html', project=project, project_comments=project_comments, worklogs=worklogs, listManager=listManager, current_user_objectid=current_user_objectid, project_creator=project_creator)
    else:
        if 'addComment' in request.form:
            person_id = person_operations.GetPerson(current_user, current_user.email)[0]
            commented_project_id = int(key)
            comment = request.form['project_comment']
            create_date = datetime.datetime.now()
            update_date = datetime.datetime.now()
            project_comment = ProjectComment(None, person_id, commented_project_id, comment, create_date, update_date)
            store_comments.add_project_comment(project_comment)
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'update' in request.form:
            title = request.form['project_name']
            project_description = request.form['project_description']
            end_date = datetime.datetime.now() #datepicker eklenince düzeltilecek
            member_limit = request.form['limit']
            manager = request.form['project_manager']
            deleted = '0'
            store.update_project(int(key), title, project_description, end_date, member_limit, manager, deleted)
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'delete_project' in request.form:
            store.delete_project(int(key))
            return redirect(url_for('site.home_page'))
        elif 'delete' in request.form:
            comment_key = request.form['delete']
            store_comments.delete_project_comment(int(comment_key))
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'edit' in request.form:
            comment_key = request.form['edit']
            new_comment = request.form['newComment']
            store_comments.update_project_comment(comment_key, new_comment, False)
            return redirect(url_for('site.projects_details_page', key=key))





