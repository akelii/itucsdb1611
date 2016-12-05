from flask import render_template
import os
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from classes.operations.work_log_operations import work_log_operations
from classes.operations.project_operations import project_operations

def home_page_config(request):
    store_worklogs = work_log_operations()
    worklogs = store_worklogs.GetFollowedProjectsWorkLogs(2)
    return render_template('dashboard.html', worklogs=worklogs)
