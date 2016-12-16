from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask_login import current_user
from datetime import datetime
from classes.project_comment import ProjectComment
from classes.operations.project_operations import project_operations
from classes.operations.project_comment_operations import project_comment_operations
from classes.operations.person_operations import person_operations
from classes.project import Project
from classes.work_log import WorkLog
from classes.operations.work_log_operations import work_log_operations
from classes.look_up_tables import *
from classes.operations.team_operations import team_operations
from classes.team import Team
from classes.model_config import dsn
import psycopg2 as dbapi2

def project_details_page_config(submit_type, key):
    store = project_operations()
    store_comments = project_comment_operations()
    store_worklogs = work_log_operations()
    PersonProvider = person_operations()
    teamList = team_operations()
    if submit_type == 'GET':
        project = store.get_project(key)
        listManager = GetManagerList()
        project_comments = store_comments.get_project_comments(key)
        listPerson = PersonProvider.GetPersonList()
        members = teamList.GetAllMembersByProjectId(key)
        worklogs = store_worklogs.GetWorkLogByProjectId(key)
        current_user_objectid = person_operations.GetPerson(current_user, current_user.email)[0]#current_userın person tablosundaki halinin objectidsi
        project_creator = project[8]#projeyi oluşturan kişi
        return render_template('projects/project_details.html', project=project, project_comments=project_comments, members=members, worklogs=worklogs, listManager=listManager, current_user_objectid=current_user_objectid, project_creator=project_creator, listPerson=listPerson)
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
        elif 'addMember' in request.form:
            teamMember = request.form.getlist('teamMember')
            # newMemberPersonId = request.form['newMemberPersonId']
            # newMemberProjectId = request.form['newMemberProjectId']
            # newMemberDuty = request.form['newMemberDuty']
            # teamList.AddTeam(newMemberProjectId, newMemberPersonId, newMemberDuty)
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'updateMember' in request.form:
            updateMemberPersonId = request.form['updateMemberPersonId']
            updateMemberProjectId = request.form['updateMemberProjectId']
            updateMemberDuty = request.form['updateMemberDuty']
            updateMemberId = request.form['updateMemberId']
            teamList.UpdateTeam(updateMemberId, updateMemberPersonId, updateMemberProjectId, updateMemberDuty)
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'deleteMember' in request.form:
            deleteMemberId = request.form['deleteMemberId']
            teamList.DeleteTeam(deleteMemberId)
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'addWorklog' in request.form:
            cretaorPersonId = person_operations.GetPerson(current_user, current_user.email)[0]
            projectId = key
            commitMessage = request.form['commitMessage']
            worklog = WorkLog(None, projectId, commitMessage, ' "+str(datetime.datetime.now())+" ', cretaorPersonId, False)
            store_worklogs.AddWorkLog(worklog)
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'editWorklog' in request.form:
            worklog_id = request.form['editWorklog']
            new_log = request.form['new_log']
            store_worklogs.UpdateWorkLog(worklog_id, new_log)
            return redirect(url_for('site.projects_details_page', key=key))
        elif 'deleteWorklog' in request.form:
            worklog_id = request.form['deleteWorklog']
            store_worklogs.DeleteWorkLog(worklog_id)
            return redirect(url_for('site.projects_details_page', key=key))

