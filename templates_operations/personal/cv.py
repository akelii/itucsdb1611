from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
import time
from classes.operations.CV_operations import cv_operations
from classes.operations.CVInformation_operations import cv_information_operations
from classes.CVInformation import CVInformation


def personal_cv_page_config(submit_type):
    store = cv_information_operations()
    now = datetime.now()
    if submit_type == 'GET':
        cvInformations=store.get_cv_information_s()
        return render_template('personal/cv.html',cvInformations=cvInformations, current_time=now.ctime())
    else:
        if request.form['add']=="delete":
            key =request.form['delete_id']
            store.delete_cv_information(key)
        elif request.form['add']=="update":
            key = request.form['delete_id']
            description = request.form['description']
            store.update_cv_information(key, description, None,None)
        else:
            description=request.form['description']
            idtype=request.form['add']
      #  start = time.mktime(datetime.strptime(request.form['stardate'], '%Y-%m').timetuple()) if request.form['startdate'] else None
       # end = time.mktime(datetime.strptime(request.form['enddate'],'%Y-%m').timetuple()) if request.form['enddate'] else None
            cvinfo=CVInformation(None,'1',description,idtype,None,None)

            store.add_cv_information(cvinfo)
        return redirect(url_for('site.personal_cv_page'))
