from flask import Blueprint
from flask import render_template
from flask_login.utils import login_required, login_user, current_user
from templates_operations.personal.default import *
from templates_operations.projects.create_project import *
from templates_operations.projects.search_project import*
from templates_operations.projects.project_details import*
from templates_operations.projects.project_update import *
from templates_operations.projects.project_comments import*
from templates_operations.projects.project_add_comment import*
from templates_operations.personal.cv import *
from templates_operations.register import*
from templates_operations.people.search_person import *
from templates_operations.people.person_detail import *
from templates_operations.dashboard import *

site = Blueprint('site', __name__)




@site.route('/register', methods=["GET", "POST"])
def register_page():
    return register_page_config(request)



@site.route('/personal', methods=["GET", "POST"])
def personal_default_page():
    return personal_default_page_config(request)
from flask import Flask
from flask import render_template, Blueprint
from flask import request, redirect, url_for
from datetime import datetime
import os
import re
import json
import psycopg2 as dbapi2
from handlers import site
from flask_login import LoginManager
from flask_login import login_required, login_user, current_user
from templates_operations.user import*
from passlib.apps import custom_app_context as pwd_context

from classes.operations.project_operations import project_operations
from classes.operations.person_operations import person_operations
from classes.project import Project
from classes.look_up_tables import *
from templates_operations.user import*

@site.route('/issues')
def personal_issues_page():
    return render_template('personal/current_projects.html')


@site.route('/project_create', methods=["GET", "POST"])
@login_required
def projects_create_page():
    return project_create_page_config(request.method)


@site.route('/project_search', methods=["GET", "POST"])
def projects_search_page():
    return project_search_page_config(request.method)


@site.route('/project_details/<int:key>', methods=["GET", "POST"])
def projects_details_page(key):
    return project_details_page_config(request.method, key)


@site.route('/home', methods=["GET", "POST"])
def home_page():
    return home_page_config(request)


@site.route('/people_connections')
def connections_following_people():
    return render_template('connections/following_people.html')


@site.route('/project_connections')
def connections_following_projects():
    return render_template('connections/following_projects.html')


@site.route('/cv', methods=["GET", "POST"])
def personal_cv_page():
    return personal_cv_page_config(request.method)


@site.route('/cv/<int:key>', methods=["GET", "POST"])
def personal_cv_pagewithkey(key):
    return personal_cv_pagewithkey_config(request.method, key)


@site.route('/settings')
def personal_settings_page():
    return render_template('personal/settings.html')


@site.route('/people_search', methods=["GET", "POST"])
def people_search_person_page():
    return people_search_person_page_config(request)


@site.route('/person_detail/<int:key>', methods=["GET", "POST"])
def people_person_detail_page(key):
    return people_person_detail_page_config(request, key)


@site.route('/logout')
def logout_page():
    return render_template('logout.html')


@site.route('/login')
def login_page():
    return render_template('login.html')