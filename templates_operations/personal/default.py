from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from classes.operations.person_operations import person_operations
from classes.operations.followed_person_operations import followed_person_operations

def personal_default_page_config(request):
    store = person_operations()
    if  request and 'delete' in request.form and request.method == 'POST':
        p = store.GetPersonByObjectId(request.form['delete'])
        store.DeletePerson(request.form['delete'])
    store_followedperson = followed_person_operations()
    Current_Person = store.GetPersonByObjectId(1)  # SONRADAN DUZELT
    listFollowing = store_followedperson.GetFollowedPersonListByPersonId(1)
    listFollowers = store_followedperson.GetFollowedPersonListByFollowedPersonId(1)
    listPerson = store.GetPersonList()
    now = datetime.now()
    return render_template('personal/default.html', current_time=now.ctime(), Current_Person=Current_Person,
                           listFollowing=listFollowing, listFollowers=listFollowers, listPerson=listPerson)
#if submit_type == 'GET':
#    store = followed_person_operations()
    # result = store.GetFollowedPersonByObjectId(2)
#    result = store.GetFollowedPersonList()
    # p = FollowedPerson(None, 1, 2, datetime.now())
    # store.AddFollowedPerson(p)
#    now = datetime.now()
#    return render_template('personal/default.html', current_time=now.ctime(), FollowedPersonList=result)
#from classes.operations.followed_person_operations import followed_person_operations
#from classes.followed_person import FollowedPerson
