from flask import render_template
import os
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from flask_login import current_user
from classes.operations.work_log_operations import work_log_operations
from classes.operations.project_operations import project_operations
from classes.operations.project_operations import project_operations
from classes.operations.person_operations import person_operations

def home_page_config(request):
    store_worklogs = work_log_operations()
    store_projects = project_operations()
    active_projects = store_projects.get_the_projects_of_a_person(person_operations.GetPerson(current_user, current_user.email)[0])
    worklogs = store_worklogs.GetFollowedProjectsWorkLogs(2)
    return render_template('dashboard.html', worklogs=worklogs, active_projects=active_projects)
