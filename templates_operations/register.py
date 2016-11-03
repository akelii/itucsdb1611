from flask import render_template
from flask import url_for
from flask import redirect
from flask import request
from datetime import datetime
#from selenium import webdriver
#from selenium.webdriver.support.ui import Select
#from selenium.webdriver.common.keys import Keys
from classes.operations.person_operations import person_operations
from classes.look_up_tables import *
from classes.person import Person

#driver = webdriver.Chrome()
#driver.get("http://jet2.com")
#select_title = Select(driver.find_element_by_id('title'))
#select_account = Select(driver.find_element_by_id('account'))
def register_page_config(request):
    if request.method == 'GET':
        listTitle = GetTitleList()
        listAccount = GetAccountTypeList()
        return render_template('register.html', listTitle=listTitle, listAccount=listAccount)
    else:
        if  'register' in request.form:
            store = person_operations()
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            eMail = request.form['eMail']
            pswd = request.form['pswd']
            accountType = request.form['account']
            title = request.form['title']
            p = Person(None, first_name, last_name, accountType, eMail, pswd, True, title, None, False)
            store.AddPerson(p)
            return render_template('dashboard.html')