from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from datetime import datetime
from flask_login import current_user, login_required
from classes.operations.person_operations import person_operations
from classes.operations.followed_person_operations import followed_person_operations
from classes.operations.personComment_operations import personComment_operations
from classes.followed_person import FollowedPerson
from classes.operations.CV_operations import cv_operations
from classes.operations.Experience_operations import experience_operations
from classes.operations.project_operations import project_operations
from classes.operations.followed_project_operations import followed_project_operations
from classes.operations.education_operations import education_operations
from classes.operations.skill_operations import skill_operations
from classes.operations.Experience_operations import experience_operations
from classes.operations.information_operations import information_operations
from classes.operations.language_operations import language_operations

def people_person_detail_page_config(request, key):
    PersonProvider = person_operations()
    CommentProvider = personComment_operations()
    Current_Person=PersonProvider.GetPerson(current_user.email)
    FollowedPersonProvider = followed_person_operations()
    CvProvider=cv_operations()
    ExperienceProvider=experience_operations()
    FollowedProjectProvider = followed_project_operations()
    EducationProvider = education_operations()
    SkillProvider = skill_operations()
    InformationProvider = information_operations()
    LanguageProvider = language_operations()
    if request and 'deleteComment' in request.form and request.method == 'POST':
        CommentProvider.DeleteTeam(request.form['deleteComment'])
    elif request and 'updateComment' in request.form and request.method == 'POST':
        selectedComment = request.form['updateId']
        updatedComment = request.form['updateComment']
        CommentProvider.UpdatePersonComment(selectedComment,  updatedComment)
    elif request and 'addComment' in request.form and request.method == 'POST':
        newComment = request.form['addComment']
        CommentProvider.AddPersonComment(Current_Person[0], key, newComment)
    elif request and 'follow' in request.form and request.method == 'POST':
        toAdd = FollowedPerson(None, Current_Person[0], key, None, None)
        FollowedPersonProvider.AddFollowedPerson(toAdd)
    elif request and 'unfollow' in request.form and request.method == 'POST':
        toDeletedFollowedPerson = FollowedPersonProvider.GetFollowedPersonByPersonIdAndFollowedPersonId(Current_Person[0], key)
        FollowedPersonProvider.DeletePerson(toDeletedFollowedPerson[0])
    FollowedPersonProvider = followed_person_operations()
    Active_Person = PersonProvider.GetPersonByObjectId(key)
    listFollowing = FollowedPersonProvider.GetFollowedPersonListByPersonId(key)
    listFollowers = FollowedPersonProvider.GetFollowedPersonListByFollowedPersonId(key)
    personComments = CommentProvider.GetPersonCommentsByCommentedPersonId(key)
    IsFollow = FollowedPersonProvider.GetFollowedPersonByPersonIdAndFollowedPersonId(Current_Person[0], Active_Person[0])
    activeCv = CvProvider.get_active_cv(key)
    followed_projects = FollowedProjectProvider.GetFollowedProjectListByPersonId(key)
    store_projects = project_operations()
    active_projects = store_projects.get_the_projects_of_a_person(key)
    active_project_number = len(active_projects)
    listEducation = EducationProvider.GetEducationListByActiveCVAndByPersonId(Active_Person[0])
    listSkill = SkillProvider.GetSkillByActiveCVAndByPersonId(Active_Person[0])
    listLanguage = LanguageProvider.GetAllLanguagesByActiveCVAndByPersonId(Active_Person[0])
    listInformation = InformationProvider.get_all_information_by_ActiveCV_And_PersonId(Active_Person[0])
    if activeCv:
        experiences = ExperienceProvider.get_experience_s_with_key(activeCv[0])
    else:
        experiences = 'none'
    now = datetime.now()
    return render_template('people/person_detail.html', current_time=now.ctime(), Current_Person=Current_Person, Active_Person=Active_Person,
                           listFollowing=listFollowing, listFollowers=listFollowers,
                           personComments=personComments, IsFollow=IsFollow, followed_projects=followed_projects,
                           experiences=experiences, active_projects=active_projects, active_project_number=active_project_number, listEducation=listEducation,
                           listSkill=listSkill, listLanguage=listLanguage, listInformation=listInformation)