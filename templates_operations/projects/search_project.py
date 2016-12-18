from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from datetime import datetime
from classes.operations.project_operations import project_operations
from classes.followed_project import FollowedProject
from classes.operations.followed_project_operations import followed_project_operations
from flask_login import current_user, login_required
from classes.operations.person_operations import person_operations
from classes.project import Project


def project_search_page_config(submit_type):
    store_person = person_operations()
    currentUser = store_person.GetPerson(current_user.email)
    store = project_operations()
    projects = store.get_projects()
    store_followed = followed_project_operations()
    count = len(projects)
    for i in range(0, count):
        temp = list(projects[i])
        if not store_followed.GetFollowedProjectByPersonIdAndProjectId(currentUser[0], projects[i][0]):
            temp.append(False)
        else:
            temp.append(True)
        projects[i] = tuple(temp)
    if submit_type == 'GET':
        return render_template('projects/search_project.html', projects=projects)
    else:
        if 'details' in request.form:
            key = request.form['details']
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'follow' in request.form:
            project_id = request.form['follow']
            followProject = FollowedProject(None, currentUser[0], project_id,'"+str(datetime.datetime.now())+"', False)
            store_followed.AddFollowedProject(followProject)
            return redirect(url_for('site.projects_search_page'))
        elif 'unfollow' in request.form:
            project_id = request.form['unfollow']
            delete_project = store_followed.GetFollowedProjectByPersonIdAndProjectId(currentUser[0], project_id)
            store_followed.DeleteFollowedProject(delete_project[0])
            return redirect(url_for('site.projects_search_page'))
