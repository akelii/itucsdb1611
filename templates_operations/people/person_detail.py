from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from datetime import datetime
from classes.operations.person_operations import person_operations
from classes.operations.followed_person_operations import followed_person_operations
from classes.operations.personComment_operations import personComment_operations


def people_person_detail_page_config(request, key):
    PersonProvider = person_operations()
    CommentProvider = personComment_operations()
    Current_Person=PersonProvider.GetPersonByObjectId(2) #Login olunca duzelt
    if request and 'deleteComment' in request.form and request.method == 'POST':
        CommentProvider.DeleteTeam(request.form['deleteComment'])
    elif request and 'updateComment' in request.form and request.method == 'POST':
        selectedComment = request.form['updateId']
        updatedComment = request.form['updateComment']
        CommentProvider.UpdatePersonComment(selectedComment,  updatedComment)
    elif request and 'addComment' in request.form and request.method == 'POST':
        newComment = request.form['addComment']
        CommentProvider.AddPersonComment(Current_Person[0], key, newComment)
    FollowedPersonProvider = followed_person_operations()
    Active_Person = PersonProvider.GetPersonByObjectId(key)
    listFollowing = FollowedPersonProvider.GetFollowedPersonListByPersonId(key)
    listFollowers = FollowedPersonProvider.GetFollowedPersonListByFollowedPersonId(key)
    personComments = CommentProvider.GetPersonCommentsByCommentedPersonId(key)
    RelatedPeople = CommentProvider.GetRelatedPersonsIdByCommentId(2)
    now = datetime.now()
    return render_template('people/person_detail.html', current_time=now.ctime(), Active_Person=Active_Person,
                           listFollowing=listFollowing, listFollowers=listFollowers,
                           personComments=personComments)