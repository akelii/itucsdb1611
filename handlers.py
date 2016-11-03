from flask import Blueprint, render_template
from templates_operations.personal.default import *
from templates_operations.projects.create_project import *
from templates_operations.projects.search_project import*
from templates_operations.projects.project_details import*

site = Blueprint('site', __name__)


@site.route('/')
def home_page():
    return  render_template('dashboard.html')

@site.route('/personal', methods=["GET", "POST"])
def personal_default_page():
    return personal_default_page_config(request.method)

@site.route('/issues')
def personal_issues_page():
    return render_template('personal/current_projects.html')

@site.route('/project_create', methods=["GET", "POST"])
def projects_create_page():
    return project_create_page_config(request.method)
 #   return render_template('projects/create_project.html')

@site.route('/project_search', methods=["GET", "POST"])
def projects_search_page():
    return project_search_page_config(request.method)
 #   return render_template('projects/search_project.html')


@site.route('/project_search/<int:key>', methods=["GET", "POST"])
def projects_details_page(key):
    return project_details_page_config(request.method, key)
 #   return project_details_page_config(request.method)


@site.route('/register')
def register_page():
    return render_template('register.html')

@site.route('/people_connections')
def connections_following_people():
    return render_template('connections/following_people.html')

@site.route('/project_connections')
def connections_following_projects():
    return render_template('connections/following_projects.html')

@site.route('/cv')
def personal_cv_page():
    return render_template('personal/cv.html')

@site.route('/settings')
def personal_settings_page():
    return render_template('personal/settings.html')

@site.route('/people_search')
def people_search_person_page():
    return render_template('people/search_person.html')

@site.route('/login')
def login_page():
    return render_template('login.html')

@site.route('/logout')
def logout_page():
    return render_template('logout.html')