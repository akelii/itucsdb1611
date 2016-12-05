from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from classes.operations.person_operations import person_operations
from classes.operations.followed_person_operations import followed_person_operations
from classes.operations.personComment_operations import personComment_operations
from classes.look_up_tables import *
from classes.person import Person
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def personal_default_page_config(request):
    PersonProvider = person_operations()
    Current_Person = PersonProvider.GetPersonByObjectId(1)  # LOGIN DUZELT
    comments = personComment_operations()
    if request and 'delete' in request.form and request.method == 'POST':
        p = PersonProvider.GetPersonByObjectId(request.form['delete'])
        PersonProvider.DeletePerson(request.form['delete'])
    if request and 'deleteComment' in request.form and request.method == 'POST':
        comments.DeleteTeam(request.form['deleteComment'])
    elif request and 'updateComment' in request.form and request.method == 'POST':
        selectedComment = request.form['updateId']
        updatedComment = request.form['updateComment']
        comments.UpdatePersonComment(selectedComment, updatedComment)
    elif request and 'addComment' in request.form and request.method == 'POST':
        personId = Current_Person[0]
        commentedPersonId = Current_Person[0]
        newComment = request.form['addComment']
        comments.AddPersonComment(personId, commentedPersonId, newComment)
    elif request and 'searchPeoplePage' in request.form and request.method == 'POST':
        return redirect(url_for('site.people_search_person_page'))
    elif request and 'searchProjectPage' in request.form and request.method == 'POST':
        return redirect(url_for('site.projects_search_page'))
    elif request and 'saveProfileSettings' in request.form and request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        eMail = request.form['eMail']
        pswd = request.form['pswd']
        accountType = request.form['account']
        title = request.form['title']
        file = request.files['file']
        gender = request.form['r1']
        if gender == 'male':
            gender = False
        elif gender == 'female':
            gender = True
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/user_images', filename))
        else:
            if gender == 'male':
                filename = 'noimage_male.jpg'
            else:
                filename = 'noimage_female.jpg'
        p = Person(1, first_name, last_name, accountType, eMail, pswd, gender, title, filename, False)
        PersonProvider.UpdatePerson(p)
    FollowedPersonProvider = followed_person_operations()
    listFollowing = FollowedPersonProvider.GetFollowedPersonListByPersonId(1)
    listFollowers = FollowedPersonProvider.GetFollowedPersonListByFollowedPersonId(1)
    personComments = comments.GetPersonCommentsByCommentedPersonId(Current_Person[0])
#    RelatedPeople = comments.GetRelatedPersonsIdByCommentId(2)
#    idOfPerson = RelatedPeople[0][1]
#    idOfCommentedPerson = RelatedPeople[0][0]
    listPerson = PersonProvider.GetPersonList()
    now = datetime.datetime.now()
    listTitle = GetTitleList()
    listAccount = GetAccountTypeList()
    return render_template('personal/default.html', current_time=now.ctime(), Current_Person=Current_Person,
                           listFollowing=listFollowing, listFollowers=listFollowers, listPerson=listPerson,
                           personComments=personComments,listAccount=listAccount, listTitle=listTitle)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
# if submit_type == 'GET':
#    store = followed_person_operations()
# result = store.GetFollowedPersonByObjectId(2)
#    result = store.GetFollowedPersonList()
# p = FollowedPerson(None, 1, 2, datetime.now())
# store.AddFollowedPerson(p)
#    now = datetime.now()
#    return render_template('personal/default.html', current_time=now.ctime(), FollowedPersonList=result)
# from classes.operations.followed_person_operations import followed_person_operations
# from classes.followed_person import FollowedPerson
