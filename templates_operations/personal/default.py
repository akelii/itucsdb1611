from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
from datetime import datetime
from classes.operations.followed_person_operations import followed_person_operations
from classes.followed_person import FollowedPerson


def personal_default_page_config(submit_type):
    if submit_type == 'GET':
        store = followed_person_operations()
        p = FollowedPerson(None, 1, 2, datetime.now())
        store.AddFollowedPerson(p)
        now = datetime.now()
        return render_template('personal/default.html', current_time=now.ctime())

