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
from classes.operations.followed_project_operations import followed_project_operations
from classes.operations.team_operations import team_operations
from flask_login import current_user, login_required

def home_page_config(request):
    PersonProvider = person_operations()
    Current_Person = PersonProvider.GetPerson(current_user.email)
    store_worklogs = work_log_operations()
    store_projects = project_operations()
    TeamProvider =team_operations()
    FollowedProjectProvider = followed_project_operations()
    active_projects = store_projects.get_the_projects_of_a_person(person_operations.GetPerson(current_user, current_user.email)[0])
    count = 0
    while (count < len(active_projects)):
        temp = list(active_projects[count])
        temp.append(list(TeamProvider.GetAllMembersByProjectId(active_projects[count][3])))
        temp.append(len(FollowedProjectProvider.GetFollowerPersonListByFollowedProjectId(active_projects[count][3])))
        active_projects[count] = tuple(temp)
        count = count + 1
    worklogs = store_worklogs.GetFollowedProjectsWorkLogs(Current_Person[0])
    return render_template('dashboard.html', worklogs=worklogs, active_projects=active_projects)
