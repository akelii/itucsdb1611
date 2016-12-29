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

    CREATE TABLE IF NOT EXISTS Project(
        | ObjectId SERIAL PRIMARY KEY,
        | Name VARCHAR(50) NOT NULL,
        | Description VARCHAR(1000) NOT NULL,
        | ProjectTypeId INTEGER NOT NULL,
        | ProjectThesisTypeId INTEGER,
        | DepartmentId INTEGER NOT NULL,
        | ProjectStatusTypeId INTEGER NOT NULL,
        | StartDate TIMESTAMP NOT NULL,
        | EndDate TIMESTAMP,
        | MemberLimit INTEGER,
        | TeamId INTEGER,
        | CreatedByPersonId INTEGER NOT NULL,
        | ProjectManagerId INTEGER NOT NULL,
        | Deleted BOOLEAN NOT NULL

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

create_project.html, project_details.html and search_project.html are related templates to the Project and they exist in **templates/project** folder.

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

    search_project.py file which exists in **template_operations/projects** folder enables an interface to show the projects. If the user is logged in, she/he can view all the projects and by clicking **Details** button, she/he can be directed to the Project Details page.
    That button's value is set by the ObjectId of the project in search_project.html.
