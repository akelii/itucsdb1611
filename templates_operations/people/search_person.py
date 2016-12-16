from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from flask_login import current_user, login_required
from classes.operations.person_operations import person_operations
from classes.operations.followed_person_operations import followed_person_operations
from classes.followed_person import FollowedPerson


def people_search_person_page_config(request):
    PersonProvider = person_operations()
    FollowedPersonProvider = followed_person_operations()
    Current_Person = PersonProvider.GetPerson(current_user.email)
    listPerson = PersonProvider.GetPersonListExcludePersonId(Current_Person[0])
    if request and 'follow' in request.form and request.method == 'POST':
        toAdd = FollowedPerson(None,Current_Person[0], request.form['follow'], None, None)
        FollowedPersonProvider.AddFollowedPerson(toAdd)
    elif request and 'unfollow' in request.form and request.method == 'POST':
        toDeletedFollowedPerson = FollowedPersonProvider.GetFollowedPersonByPersonIdAndFollowedPersonId(Current_Person[0], request.form['unfollow'])
        FollowedPersonProvider.DeletePerson(toDeletedFollowedPerson[0])
    count = 0
    while (count < len(listPerson)):
        temp = list(listPerson[count])
        temp.append(
            len(FollowedPersonProvider.GetFollowedPersonListByFollowedPersonId(listPerson[count][0])))  # Followers
        temp.append(len(FollowedPersonProvider.GetFollowedPersonListByPersonId(listPerson[count][0])))  # Following
        if not FollowedPersonProvider.GetFollowedPersonByPersonIdAndFollowedPersonId(Current_Person[0],
                                                                                     listPerson[count][0]):
            temp.append(False)  # Emtpy #O kisiyi takip etmiyor yani buton follow olacak
        else:
            temp.append(True)  # Full #O kisiyi takip ediyor yani buton unfollow olacak
        listPerson[count] = tuple(temp)
        count = count + 1
    return render_template('people/search_person.html', listPerson=listPerson)
