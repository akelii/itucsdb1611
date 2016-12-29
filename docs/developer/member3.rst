Parts Implemented by Gülçin Baykal
================================

*******
Project
*******

Table
-------

Project table exists in server.py file.

ObjectId attribute holds the primary key of the Project table.

TeamId attribute references Team table's ProjectId attribute.

ObjectId attribute references Worklog table's ProjectId attribute.

ObjectId attribute references FollowedProject table's FollowedProjectId attribute.

    .. code-block:: python

        CREATE TABLE IF NOT EXISTS Project(
            ObjectId SERIAL PRIMARY KEY,
            Name VARCHAR(50) NOT NULL,
            Description VARCHAR(1000) NOT NULL,
            ProjectTypeId INTEGER NOT NULL,
            ProjectThesisTypeId INTEGER,
            DepartmentId INTEGER NOT NULL,
            ProjectStatusTypeId INTEGER NOT NULL,
            StartDate TIMESTAMP NOT NULL,
            EndDate TIMESTAMP,
            MemberLimit INTEGER,
            TeamId INTEGER,
            CreatedByPersonId INTEGER NOT NULL,
            ProjectManagerId INTEGER NOT NULL,
            Deleted BOOLEAN NOT NULL

Class
-----

Project class exists in project.py file which is in **classes** folder.

.. code-block:: python

    class Project:
    def __init__(self, objectid, title, project_description, project_type, project_thesis_type, department, project_status_type, start_date, end_date, member_limit, team, created_by, manager):
        self.objectid = objectid
        self.title = title
        self.project_description = project_description
        self.project_type = project_type
        self.project_thesis_type = project_thesis_type
        self.department = department
        self.project_status_type = project_status_type
        self.start_date = start_date
        self.end_date = end_date
        self.member_limit = member_limit
        self.team = team
        self.created_by = created_by
        self.manager = manager
        self.deleted = 0

Class Operations
----------------
Project's class operations exists in project_operations.py which is in **classes/operations** folder.

- The following database operations are implemented for Project:
    -Add Operation

    .. code-block:: python

        def add_project(self, Project):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO Project(Name, Description, ProjectTypeId, ProjectThesisTypeId, DepartmentId, ProjectStatusTypeId, StartDate, EndDate, MemberLimit, CreatedByPersonId, ProjectManagerId, Deleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, False )",
                    (Project.title, Project.project_description, Project.project_type, Project.project_thesis_type,
                     Project.department, Project.project_status_type, Project.start_date, Project.end_date,
                     Project.member_limit, Project.created_by, Project.manager))
                connection.commit()
                self.last_key = cursor.lastrowid

    add_project takes a project as a parameter and inserts parameter project's attributes to the project which will be added to Project Table.

    -Delete Operation

    .. code-block:: python

        def delete_project(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute("""DELETE FROM Project WHERE (ObjectId=%s)""", (key,))
                connection.commit()

    delete_project takes a key value which is the ObjectId of the project to be deleted and removes that project from Project table.

    -Update Operation

    .. code-block:: python

        def update_project(self, key, title, project_description, end_date, member_limit, manager, deleted):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """UPDATE Project SET Name = %s, Description = %s, EndDate = %s, MemberLimit = %s, ProjectManagerId = %s, Deleted = %s WHERE (ObjectId=%s)""",
                    (title, project_description, end_date, member_limit, manager, deleted, key))
                connection.commit()

    update_project takes title, description, end date, member limit, manager, deleted and key values as parameters and updates the project whose ObjectId is the key, with the given attributes.

    -Get Operations

    .. code-block:: python

        def get_project(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT Project.Name, Project.Description, ProjectType.Name, Department.Name, ProjectStatusType.Name, Person.FirstName, Person.LastName, Project.ObjectId, Project.CreatedByPersonId, Project.EndDate, Project.MemberLimit FROM Project
                                  JOIN ProjectType ON(Project.ProjectTypeId=ProjectType.ObjectId)
                                  JOIN Department ON(Project.DepartmentId = Department.ObjectId)
                                  JOIN ProjectStatusType ON(Project.ProjectStatusTypeId=ProjectStatusType.ObjectId)
                                  JOIN Person ON(Project.CreatedByPersonId=Person.ObjectId)
                                  WHERE (Project.ObjectID = %s)"""
                cursor.execute(query, (key,))
                project = cursor.fetchone()
                connection.commit()
            return project

    get_project takes a key value as parameter and returns the project's name, description, type, department, status, creator's name, end date and member limit which has the same ObjectId with the key.

    .. code-block:: python

        def get_projects(self):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT Project.ObjectId, Project.Name, Description, Department.Name, Person.FirstName, Person.LastName
                                  FROM Project JOIN Department ON(Project.DepartmentId = Department.ObjectId) JOIN Person ON(Person.ObjectId = Project.ProjectManagerId)""")
                projects = cursor.fetchall()
                connection.commit()
            return projects


    get_projects returns all projects' names, descriptions, departments and managers' names in the Project table.

    .. code-block:: python

        def get_the_projects_of_a_person(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT Project.Name, Project.Description, ProjectType.Name, Project.ObjectId FROM Project
                                  JOIN ProjectType ON(Project.ProjectTypeId=ProjectType.ObjectId)
                                  JOIN Team ON(Project.ObjectId = Team.ProjectId)
                                  WHERE (Team.MemberId = %s)"""
                cursor.execute(query, (key,))
                project_ids = cursor.fetchall()
                connection.commit()
            return project_ids
   get_the_projects_of_a_person takes a key as a parameter and returns the projects' names, descriptions and types of a person which has the ObjectId same with the key.

Templates
---------

create_project.html, project_details.html and search_project.html are the related templates to the Project and they exist in **templates/project** folder.

GET/POST Operations
-------------------

-Adding a Project

    .. code-block:: python

        def project_create_page_config(submit_type):
            if submit_type == 'GET':
                listProjectType = GetProjectType()
                listProjectThesisType = GetProjectThesisType()
                listDepartment = GetDepartment()
                listProjectStatusType = GetProjectStatusType()
                listManager = GetManagerList()
                return render_template('projects/create_project.html', listProjectType=listProjectType, listProjectThesisType=listProjectThesisType, listDepartment=listDepartment, listProjectStatusType=listProjectStatusType, listManager=listManager)
            else:
                if 'Add' in request.form.values():
                    store = project_operations()
                    title = request.form['project_name']
                    project_description = request.form['project_description']
                    project_type = request.form['project_type']
                    project_thesis_type = request.form['project_thesis_type']
                    department = request.form['department']
                    start_date = request.form['start']
                    #start_date = None
                    end_date = request.form['end_date']
                    if end_date > str(datetime.datetime.now()):#ileri tarihte bitecekse
                        project_status_type = 2
                    else:#süre bitmişse
                        project_status_type = 3
                    member_limit = request.form['limit']
                    created_by = person_operations.GetPerson(current_user, current_user.email)[0]#current_user proje oluşturuyor
                    manager = request.form['project_manager']
                    project = Project(None, title, project_description, project_type, project_thesis_type, department,
                                      project_status_type, start_date, end_date, member_limit, None, created_by, manager)
                    store.add_project(project)
                    return redirect(url_for('site.home_page'))

    create_project.py file which exist in **template_operations/projects** folder enables an interface to create a project.
    When the page is opened by @site.route('/project_create', methods=["GET", "POST"]), text areas to fill and dropdown lists for static tables are shown if login requirements are satisfied. To obtain that lists, below functions are written.

    .. code-block:: python

        def GetProjectType():
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT ObjectId, Name, Deleted FROM ProjectType WHERE Deleted = FALSE"""
                cursor.execute(query)
                results = cursor.fetchall()
            return results

        def GetProjectThesisType():
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT ObjectId, Name, Deleted FROM ProjectThesisType WHERE Deleted = FALSE"""
                cursor.execute(query)
                results = cursor.fetchall()
            return results

        def GetDepartment():
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT ObjectId, Name, Deleted FROM Department WHERE Deleted = FALSE"""
                cursor.execute(query)
                results = cursor.fetchall()
            return results

        def GetProjectStatusType():
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT ObjectId, Name, Deleted FROM ProjectStatusType WHERE Deleted = FALSE"""
                cursor.execute(query)
                results = cursor.fetchall()
            return results

        def GetManagerList():
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT ObjectId, FirstName || ' ' || LastName as FullName FROM Person WHERE Deleted = FALSE"""
                cursor.execute(query)
                results = cursor.fetchall()
            return results

    If a project is wanted to be created, necessary attributes are obtained by the fields in create_project.html. After obtaining the attributes, a new project is created and added to the Project table.
    After addition, the user is directed to the home page.

    -Deleting a Project

    .. code-block:: python

        elif 'delete_project' in request.form:
            store.delete_project(int(key))
            return redirect(url_for('site.home_page'))

    project_details.py file which exists in **template_operations/projects** folder enables an interface to delete a project. If the user is the creator of the project, she/he can see the Setting tab and by clicking **Delete** button, she/he can delete the project.
    That button's value is set by the ObjectId of the project in project_details.html.
    After deletion, the user is directed to the home page.

    -Updating a Project

    .. code-block:: python

        elif 'update' in request.form:
            title = request.form['project_name']
            project_description = request.form['project_description']
            end_date = request.form['updated_date']
            member_limit = request.form['limit']
            manager = request.form['project_manager']
            deleted = '0'
            store.update_project(int(key), title, project_description, end_date, member_limit, manager, deleted)
            return redirect(url_for('site.projects_details_page', key=key))

    project_details.py file which exists in **template_operations/projects** folder enables an interface to update a project. If the user is the creator of the project, she/he can see the Setting tab and by clicking **Update** button, a modal pops up. After filling the places, she/he can update the project.
    That button's value is set by the ObjectId of the project in project_details.html.
    After updating, the user is directed to the details page again.

    -Getting the Projects

    .. code-block:: python

        def project_search_page_config(submit_type):
            projects = store.get_projects()
            if submit_type == 'GET':
                return render_template('projects/search_project.html', projects=projects)
            else:
                if 'details' in request.form:
                    key = request.form['details']
                    return redirect(url_for('site.projects_details_page', key=key))

    search_project.py file which exists in **template_operations/projects** folder enables an interface to show the projects. If the user is logged in and got to the page by @site.route('/project_search', methods=["GET", "POST"]) , she/he can view all the projects and by clicking **Details** button, she/he can be directed to the Project Details page and get to @site.route('/project_details/<int:key>', methods=["GET", "POST"]).
    That button's value is set by the ObjectId of the project in search_project.html.

***************
Project Comment
***************

Table
------

ProjectComment table exists in server.py file.

ObjectId attribute holds the primary key of the ProjectComment table.

.. code-block:: python

    CREATE TABLE IF NOT EXISTS ProjectComment(
        ObjectId SERIAL PRIMARY KEY,
        PersonId INTEGER NOT NULL,
        CommentedProjectId INTEGER NOT NULL,
        Comment VARCHAR(500) NOT NULL,
        CreateDate TIMESTAMP NOT NULL,
        UpdateDate TIMESTAMP NOT NULL,
        Deleted BOOLEAN NOT NULL

Class
-----

ProjectComment class exists in project_comment.py file which is in **classes** folder.

.. code-block:: python

    class ProjectComment:
    def __init__(self, ObjectId, PersonId, CommentedProjectId, Comment, CreateDate, UpdateDate):
        self.ObjectId = ObjectId
        self.PersonId = PersonId
        self.CommentedProjectId = CommentedProjectId
        self.Comment = Comment
        self.CreateDate = CreateDate
        self.UpdateDate = UpdateDate
        self.Deleted = 0

Class Operations
----------------
ProjectComment's class operations exists in project_comment_operations.py which is in **classes/operations** folder.

- The following database operations are implemented for ProjectComment:
    -Add Operation

    .. code-block:: python

        def add_project_comment(self, ProjectComment):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO ProjectComment(PersonId, CommentedProjectId, Comment, CreateDate, UpdateDate, Deleted) VALUES (%s, %s, %s, ' "+str(datetime.datetime.now())+"', ' "+str(datetime.datetime.now())+"', False)",
                    (ProjectComment.PersonId, ProjectComment.CommentedProjectId, ProjectComment.Comment))
                connection.commit()
                self.last_key = cursor.lastrowid

    add_project_comment takes a project comment as a parameter and inserts parameter project comment's attributes to the project comment which will be added to ProjectComment Table.

    -Delete Operation

    .. code-block:: python

        def delete_project_comment(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute("""DELETE FROM ProjectComment WHERE (ObjectId=%s)""", (key,))
                connection.commit()

    delete_project_comment takes a key value which is the ObjectId of the project comment to be deleted and removes that project comment from ProjectComment table.

    -Update Operation

    .. code-block:: python

        def update_project_comment(self, key, Comment, Deleted):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """UPDATE ProjectComment SET Comment = %s, UpdateDate = NOW(), Deleted = %s WHERE (ObjectId=%s)""",
                    (Comment, Deleted, key))
                connection.commit()

    update_project_comment takes comment, deleted and key values as parameters and updates the project comment whose ObjectId is the key, with the given attributes.

    -Get Operation

    .. code-block:: python

        def get_project_comments(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT Person.FirstName,Person.LastName, ProjectComment.Comment,ProjectComment.CreateDate, ProjectComment.ObjectId, Person.ObjectId, ProjectComment.UpdateDate
                                  FROM ProjectComment
                                  JOIN Project ON(Project.ObjectId=ProjectComment.CommentedProjectId)
                                  JOIN Person ON(Person.ObjectId=ProjectComment.PersonId)
                                  WHERE (ProjectComment.CommentedProjectId=%s) ORDER BY ProjectComment.CreateDate DESC""", (key,))
                project_comments = cursor.fetchall()
                connection.commit()
            return project_comments

    get_project_comments takes a key value as parameter and returns the project's comments by descending order, which has the same ObjectId with the key.

Templates
---------

project_details.html is the related template to the ProjectComment and it exists in **templates/project** folder.

GET/POST Operations
-------------------

    -Adding a ProjectComment

    .. code-block:: python

        if 'addComment' in request.form:
            person_id = person_operations.GetPerson(current_user, current_user.email)[0]
            commented_project_id = int(key)
            comment = request.form['project_comment']
            create_date = datetime.datetime.now()
            update_date = datetime.datetime.now()
            project_comment = ProjectComment(None, person_id, commented_project_id, comment, create_date, update_date)
            store_comments.add_project_comment(project_comment)
            return redirect(url_for('site.projects_details_page', key=key))

    project_details.py file which exists in **template_operations/projects** folder enables an interface to add a project comment in Project's Comments tab.
    After clicking **Add Comment** button, the comment will be posted and the user will be redirected to Project's Detail page.

    -Deleting a ProjectComment

    .. code-block:: python

        elif 'delete' in request.form:
            comment_key = request.form['delete']
            store_comments.delete_project_comment(int(comment_key))
            return redirect(url_for('site.projects_details_page', key=key))

    project_details.py file which exists in **template_operations/projects** folder enables an interface to delete a project comment in Project's Comments tab.
    If the current_user is the creator of the comment, **Delete** button will be shown below that comment.
    After deletion, the user will be redirected to Project's Detail page.

    -Updating a ProjectComment

    .. code-block:: python

        elif 'edit' in request.form:
            comment_key = request.form['edit']
            new_comment = request.form['newComment']
            store_comments.update_project_comment(comment_key, new_comment, False)
            return redirect(url_for('site.projects_details_page', key=key))

    project_details.py file which exists in **template_operations/projects** folder enables an interface to update a project comment in Project's Comments tab.
    If the current_user is the creator of the comment, a pencil shaped button will be shown below that comment and a tex area to enter the new comment will pop up.
    After updating the comment, the update date will be changed and the user will be redirected to Project's Detail page.

    -Getting the ProjectComments

    .. code-block:: python

        def project_details_page_config(submit_type, key):
            store_comments = project_comment_operations()
            current_person = PersonProvider.GetPerson(current_user.email)
            if submit_type == 'GET':
                project_comments = store_comments.get_project_comments(key)
                current_user_objectid = person_operations.GetPerson(current_user, current_user.email)[0]#current_userın person tablosundaki halinin objectidsi
                project_creator = project[8]#projeyi oluşturan kişi
                return render_template('projects/project_details.html', project=project, project_comments=project_comments,
                                       members=members, worklogs=worklogs, listManager=listManager, isFollow=isFollow,
                                       current_user_objectid=current_user_objectid, project_creator=project_creator, listPerson=listPerson)

    project_details.py file which exists in **template_operations/projects** folder enables an interface to show a project's all comment in Project's Comments tab.
    A timeline including the comments of the project are listed in descending order by create date of the comments.


***********
Information
***********

Table
------

Information table exists in server.py file.

ObjectId attribute holds the primary key of the Information table.

.. code-block:: python

    CREATE TABLE IF NOT EXISTS Information (
        ObjectId SERIAL PRIMARY KEY,
        CVId INTEGER NOT NULL,
        InformationTypeId INTEGER NOT NULL,
        Description VARCHAR(500) NOT NULL,
        Deleted BOOLEAN NOT NULL

Class
-----

Information class exists in information.py file which is in **classes** folder.

.. code-block:: python

    class Information:
        def __init__(self, objectid, cvid, information_type_id, description):
            self.objectid = objectid
            self.cvid = cvid
            self.information_type_id = information_type_id
            self.description = description
            self.deleted = 0

Class Operations
----------------
Information's class operations exists in information_operations.py which is in **classes/operations** folder.

- The following database operations are implemented for Information:
    -Add Operation

    .. code-block:: python

        def add_information(self, informationCVId, information_type_id, description):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "INSERT INTO Information (CVId, InformationTypeId, Description, Deleted) VALUES (%s, %s, %s, False)"
                cursor.execute(query, (informationCVId, information_type_id, description))
                connection.commit()
                self.last_key = cursor.lastrowid

    add_information takes information's CV id, information's type id and description as parameters and inserts the attributes to the Information Table.

    -Delete Operation

    .. code-block:: python

        def delete_information(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """DELETE FROM Information WHERE (ObjectId=%s)"""
                cursor.execute(query, (key,))
                connection.commit()

    delete_information takes a key value which is the ObjectId of the information to be deleted and removes that information from Information table.

    -Update Operation

    .. code-block:: python

        def update_information(self, key, description):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """UPDATE Information SET Description = %s WHERE (ObjectId=%s)""",
                    (description, key))
                connection.commit()

    update_information takes description and key values as parameters and updates the information whose ObjectId is the key, with the given attribute.

    -Get Operation

    .. code-block:: python

        def get_all_information_by_CVId(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT Information.ObjectId, Information.CVId, InformationType.Name, Information.Description FROM Information JOIN CV ON(Information.CVId = CV.ObjectId) JOIN InformationType ON(Information.InformationTypeId = InformationType.ObjectId) WHERE (CV.ObjectId = %s)"""
                cursor.execute(query, (key,))
                results = cursor.fetchall()
            return results

    get_all_information_by_CVId takes a key value as parameter and returns related CV's information, which has the same ObjectId with the key.

Templates
---------

cv.html is the related template to the Information and it exists in **templates/personal** folder.

GET/POST Operations
-------------------

    -Adding an Info

    .. code-block:: python

        elif request and 'information_desc' in request.form and request.method == 'POST':
            information_type_id = request.form['information_type']
            information_desc = request.form['information_desc']
            information_store.add_information(key, information_type_id, information_desc)
            allInformation = information_store.get_all_information_by_CVId(key)
            updateCV = "TRUE"

    cv.py file which exists in **template_operations/personal** folder enables an interface to add an info.

    .. code-block:: python

        def GetInformationTypeList():
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT ObjectId, Name, Deleted FROM InformationType WHERE Deleted = FALSE"""
                cursor.execute(query)
                results = cursor.fetchall()
            return results

    Different types of information are available and can be listed by the above function which is in look_op_tables.py

    After clicking **Add** button in **Information** section, a modal will be pop up and by clicking **Save** button, new info will be added to your CV.
    After addition, the user will be redirected to Personal CV page with the address @site.route('/cv/<int:key>',methods=["GET", "POST"]).

    -Deleting an Info

    .. code-block:: python

        elif request and 'deleteInformation' in request.form and request.method == 'POST':
            deletionIndex = request.form['deleteInformation']
            information_store.delete_information(deletionIndex)
            allInformation = information_store.get_all_information_by_CVId(key)
            updateCV = "TRUE"

    cv.py file which exists in **template_operations/personal** folder enables an interface to delete an info.
    By clicking **cross** symbol, a warning will pop up asking whether the user is sure to delete the info or not.
    After deletion, the user will be redirected to Personal CV page.

    -Updating an Info

    .. code-block:: python

        elif request and 'updateInformationDesc' in request.form and request.method == 'POST':
            updatedInformationDescription = request.form['updateInformationDesc']
            InformationId = request.form['updateInformationId']
            information_store.update_information(InformationId, updatedInformationDescription)
            allInformation = information_store.get_all_information_by_CVId(key)
            updateCV = "TRUE"

    cv.py file which exists in **template_operations/personal** folder enables an interface to update an info.
    By clicking **pencil** symbol, a modal will pop up asking new description.
    After updating, the user will be redirected to Personal CV page.

    -Getting the Information

    .. code-block:: python

        def personal_cv_pagewithkey_config(submit_type, key):
            listInformation = GetInformationTypeList()
            information_store = information_operations()
            allInformation = information_store.get_all_information_by_CVId(key)
            updateCV="False"
            return render_template('personal/cv.html', cvs=cvs,CurrentCV=CurrentCV, languages = allLanguages, experiences=experiences, listEducation=listEducation,
                                   current_time=now.ctime(), informationn=allInformation, listInformation=listInformation, skills=skills)

    cv.py file which exists in **template_operations/personal** folder enables an interface to show all information of a CV in Information section.

*******
Others
*******

**In this page, functions which have common necessities by all members and implemented by Gülçin Baykal are introduced.**

    .. code-block:: python

        def GetPerson(self, userEMail):#current_userın emaili ile person tablosundaki haline ulaşıyoruz
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT Person.ObjectId, FirstName || ' ' || LastName as FullName, AccountType.AccountTypeName, Email, Password, Gender, Title.Name, PhotoPath, FirstName, LastName
                            FROM Person
                            INNER JOIN AccountType ON (Person.AccountTypeId = AccountType.ObjectId)
                            INNER JOIN Title ON (Person.TitleId = Title.ObjectId)
                            WHERE eMail = %s"""
                cursor.execute(query, (userEMail,))
                person_id = cursor.fetchone()
            return person_id

    This function is used to obtain the current user's extra information which are saved in Person table, by the current_user's email. It can be found in person_operations.py file

    .. code-block:: python

        class User(UserMixin):
            def __init__(self, email, password):
                self.email = email
                self.password = password
                self.active = True


            def get_id(self):
                return self.email

            @property
            def is_active(self):
                return self.active


        def AddUser(user):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "INSERT INTO Users (Email, Password, Deleted) VALUES (%s, %s, FALSE )"
                cursor.execute(query, (user.email, user.password))
                connection.commit()

    This class is created for login operations since only the email and password is asked to user to type. It can be found in user.py file.