from flask import render_template
from flask import redirect
from flask import request
from datetime import datetime
from datetime import datetime
from classes.operations.project_operations import project_operations
from classes.project import Project
from classes.model_config import dsn
import psycopg2 as dbapi2

def project_details_page_config(submit_type, key):
    store = project_operations()
    if submit_type == 'GET':
        project = store.get_project(key)
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT Name, Description FROM Project WHERE (ObjectID=%s)""", (key,))
            project = cursor.fetchone()
            connection.commit()
        return render_template('projects/project_detail.html',project=project)
    else:
        if 'update' in request.form:
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
            deleted = '0'
            store.update_project(int(key), title, project_description, project_type, project_thesis_type, department, project_status_type, start_date, end_date, member_limit, None, created_by, manager, deleted )
            return render_template('dashboard.html')



