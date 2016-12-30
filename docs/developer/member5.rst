Parts Implemented by Mehmet Barış Yaman
=======================================

********
Language
********

Table
-----

Language table exists in server.py file.

ObjectId attribute holds the primary key of the Language table.

CVId is the foreign key that is connected to CV.ObjectId

    .. code-block:: python

        CREATE TABLE IF NOT EXISTS Language(
                ObjectId SERIAL PRIMARY KEY,
                CVId INTEGER NOT NULL,
                Name VARCHAR(50) NOT NULL,
                Level VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )

        cursor.execute("""ALTER TABLE Language ADD FOREIGN KEY(CVId) REFERENCES CV(ObjectId) ON DELETE CASCADE """)


Class
-----

Language class exists in language.py file which is in **classes** folder.

.. code-block:: python

    class Language:
    def __init__(self, objectId, cvId, name, level):
        self.ObjectId = objectId
        self.CVId = cvId
        self.Name = name
        self.Level = level
        self.Deleted = 0

Class Operations
----------------
Language class operations exists in language_operations.py which is in **classes/operations** folder.

- The following database operations are implemented for Language Class:
    -Add Operation

    .. code-block:: python

        def AddLanguage(self, languageCVId, languageName, languageLevel):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "INSERT INTO Language (CVId, Name, Level, Deleted) VALUES (%s, %s, %s, False)"
                cursor.execute(query, (languageCVId, languageName, languageLevel))
                connection.commit()
                self.last_key = cursor.lastrowid

    AddLanguage function inserts a new tuple into the database taking languageName and languageLevel parameters from the user, CVId from interface

    -Delete Operation

    .. code-block:: python

        def DeleteLanguage(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """DELETE FROM Language WHERE (ObjectId=%s)"""
                cursor.execute(query, (key,))
                connection.commit()

    DeleteLanguage simply deletes the language from database taking ObjectId as parameter.

    -Update Operation

    .. code-block:: python

        def UpdateLanguage(self, key, name, level ):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """UPDATE Language SET Name = %s, Level = %s WHERE (ObjectId=%s)""",
                    (name, level, key))
                connection.commit()

    UpdateLanguage takes name and level parameters from the user and take the key parameter from the interface and updates the tuple corresponding to key.

    -Get Operations

    .. code-block:: python

        # Returns one language selected by CVId and Name
        def GetLanguageByName(self, nameKey, idKey):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT Language.Name, Language.Level FROM Language INNER JOIN CV ON(Language.CVId = CV.ObjectId)WHERE (Language.Name = %s AND CV.ObjectId = %s) """
                cursor.execute(query, (nameKey,idKey))
                result = cursor.fetchall()
            return result

    GetLanguageByName takes nameKey from user and idKey from interface, returns the language selected by name and CVId.

    .. code-block:: python

        # Returns all languages selected by CVId
        def GetAllLanguagesByCVId(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT Language.ObjectId, Language.CVId, Language.Name, Language.Level FROM Language INNER JOIN CV ON(Language.CVId = CV.ObjectId) WHERE (CV.ObjectId = %s)"""
                cursor.execute(query, (key,))
                result = cursor.fetchall()
            return result

        def GetAllLanguagesByActiveCVAndByPersonId(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT Language.ObjectId, Language.CVId, Language.Name, Language.Level
                            FROM Language
                            INNER JOIN CV ON (Language.CVId = CV.ObjectId)
                            INNER JOIN Person ON (CV.PersonId = Person.ObjectId)
                            WHERE (Language.CVId=(Select CV.ObjectId FROM CV
                                                  INNER JOIN Person ON (CV.PersonId = Person.ObjectId)
                                                  WHERE (Person.ObjectId = %s AND CV.IsActive=TRUE)))"""
                cursor.execute(query, (key,))
                result = cursor.fetchall()
            return result

   GetAllLanguagesByActiveCVAndByPersonId returns all languages and all language's attributes of a person if the person's CV is active

Templates
---------

cv.html is the related template for Language Table existing in **templates/personal** folder.

GET/POST Operations
-------------------

    -Adding a Language

    .. code-block:: python

        elif request and 'newLanguageName' in request.form and request.method == 'POST':
               newLanguageName = request.form['newLanguageName']
               newLevel = request.form['newLanguageLevel']
               languages.AddLanguage(key, newLanguageName, newLevel)
               allLanguages = languages.GetAllLanguagesByCVId(key)
               updateCV = "TRUE"



    -Deleting a Language

    .. code-block:: python

        if request and 'deleteLanguage' in request.form and request.method == 'POST':
            deleteIndex = request.form['deleteLanguage']
            languages.DeleteLanguage(deleteIndex)
            allLanguages = languages.GetAllLanguagesByCVId(key)
            updateCV = "TRUE"

    When the user presses the "x" button near the language the index is obtained by the hidden input from the cv.html.

    Therefore, user does not see the ObjectId's of the tuples, but ids come with a request.

    After that, all languages are still need to be gotten since there is a change with the deletion.

    -Updating a Language

    .. code-block:: python

        elif request and 'updateLanguageName' in request.form and request.method == 'POST':
             updateName = request.form['updateLanguageName']
             updateLevel = request.form['updateLanguageLevel']
             ID = request.form['updateLanguageId']
             languages.UpdateLanguage(ID, updateName, updateLevel)
             allLanguages = languages.GetAllLanguagesByCVId(key)
             updateCV = "TRUE"


    With the another button near 'x' button in each languages that are shown, the user enters the information and those informations are held and sent to the update table operation.

    After that, all languages are gotten with a key for showing the change.

    -Getting the Languages

    .. code-block:: python

        def personal_cv_pagewithkey_config(submit_type, key):
            languages = language_operations()
            allLanguages = languages.GetAllLanguagesByCVId(key)
            return render_template('personal/cv.html', cvs=cvs,CurrentCV=CurrentCV, languages = allLanguages, experiences=experiences, listEducation=listEducation,
                                   current_time=now.ctime(), informationn=allInformation, listInformation=listInformation, skills=skills)


    All languages are gotten after each operation and render_template is used since no change has to be made for the address of page.

    Basicly all changes will be shown to user after each operation.

**************
Person Comment
**************

Table
-----

PersonComment table exists in server.py file.

ObjectId attribute holds the primary key of the PersonComment table.

PersonId and CommentedPersonId are foreign keys connected to Person.ObjectId

.. code-block:: python

        query = """CREATE TABLE IF NOT EXISTS PersonComment(
                ObjectId SERIAL PRIMARY KEY,
                PersonId INTEGER NOT NULL,
                CommentedPersonId INTEGER NOT NULL,
                Comment VARCHAR(500) NOT NULL,
                CreateDate TIMESTAMP NOT NULL,
                UpdateDate TIMESTAMP NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""

        cursor.execute(
            """ALTER TABLE PersonComment ADD FOREIGN KEY(CommentedPersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE """)
        cursor.execute(
            """ALTER TABLE PersonComment ADD FOREIGN KEY(PersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE """)

Class
-----

PersonComment class exists in personComment.py file which is in **classes** folder.

.. code-block:: python

    class PersonComment:
        def __init__(self, objectId, personId, commentedPersonId, comment, createDate, updateDate):
            self.ObjectId = objectId
            self.PersonId = personId
            self.CommentedPersonId = commentedPersonId
            self.Comment = comment
            self.CreateDate = createDate
            self.UpdateDate = updateDate
            self.Deleted = 0


Class Operations
----------------
PersonComment Class operations exist in personComment_operations.py which is in **classes/operations** folder.

- The following database operations are implemented for PersonComment:

    -Add Operation

    .. code-block:: python

        def AddPersonComment(self, personId, commentedPersonId, comment):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "INSERT INTO PersonComment (PersonId, CommentedPersonId, Comment, CreateDate, UpdateDate, Deleted) VALUES (%s, %s, %s, ' "+str(datetime.datetime.now())+"', ' "+str(datetime.datetime.now())+"', False)"
                cursor.execute(query, (personId, commentedPersonId, comment))
                connection.commit()
                self.last_key = cursor.lastrowid

    addPersonComment function takes comment form user and the ids from the interface (hidden input)

    Then the function inserts a comment to the database accordingly.

    -Delete Operation

    .. code-block:: python

        def DeleteTeam(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """DELETE FROM PersonComment WHERE (ObjectId=%s)"""
                cursor.execute(query, (key,))
                connection.commit()

    DeleteTeam function takes a key value as hidden input and deletes the tuple accordingly

    -Update Operation

    .. code-block:: python

        def UpdatePersonComment(self, key, comment ):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """UPDATE PersonComment SET  Comment = %s, UpdateDate = NOW(), Deleted = False WHERE (ObjectId=%s)""",
                    (comment, key))
                connection.commit()

    UpdatePersonComment takes the key as hidden and new comment from the user and updates the comment in the database accordingly

    -Get Operations

    .. code-block:: python

        # Returns all comments made by a person, selected by person ID
        def GetPersonCommentsByPersonId(self, personId):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT PersonComment.ObjectId, p2.FirstName ||' '||  p2.LastName as FullName, PersonComment.Comment, PersonComment.UpdateDate, p1.ObjectId, p2.ObjectId
                           FROM PersonComment
                           INNER JOIN Person AS p1 ON(PersonComment.PersonId = p1.ObjectId)
                           INNER JOIN Person AS p2 ON(PersonComment.CommentedPersonId = p2.ObjectId)
                           WHERE (p1.ObjectId = %s)"""
                cursor.execute(query, (personId,))
                result = cursor.fetchall()
            return result

        # Returns all comments received by a person, selected by person ID
        def GetPersonCommentsByCommentedPersonId(self, commentedPersonId):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT PersonComment.ObjectId ,p1.FirstName ||' '||  p1.LastName as FullName, PersonComment.Comment, PersonComment.UpdateDate, p1.ObjectId, p2.ObjectId, p1.PhotoPath
                           FROM PersonComment
                           INNER JOIN Person AS p1 ON(PersonComment.PersonId = p1.ObjectId)
                           INNER JOIN Person AS p2 ON(PersonComment.CommentedPersonId = p2.ObjectId)
                           WHERE (p2.ObjectId = %s) ORDER BY PersonComment.CreateDate DESC"""
                cursor.execute(query, (commentedPersonId,))
                result = cursor.fetchall()
            return result

        # Returns object ids of persons that one of them comments and one of them is commented
        def GetRelatedPersonsIdByCommentId(self, commentId):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT p1.ObjectId, p2.ObjectId
                           FROM PersonComment
                           INNER JOIN Person AS p1 ON(PersonComment.PersonId = p1.ObjectId)
                           INNER JOIN Person AS p2 ON(PersonComment.CommentedPersonId = p2.ObjectId)
                           WHERE (PersonComment.ObjectId = %s)"""
                cursor.execute(query, (commentId,))
                result = cursor.fetchall()
            return result

GetPersonCommentsByPersonId and GetPersonCommentsByCommentedPersonId functions also works for the privilege that the users can adjust the tuples.

All get functions are also used for showing the tuples after each db operations.

Templates
---------

default.html is the related template to the PersonComment in **templates/personal** folder.

GET/POST Operations
-------------------

    -Adding a PersonComment

    .. code-block:: python

        if request and 'addComment' in request.form and request.method == 'POST':
            personId = Current_Person[0]
            commentedPersonId = Current_Person[0]
            newComment = request.form['addComment']
            comments.AddPersonComment(personId, commentedPersonId, newComment)

    IDs come from the person class operations since we are looking for commentedPersonId and personId as arguments.

    Additionally, newComment comes from the user.

    -Deleting a PersonComment

    .. code-block:: python

        if request and 'deleteComment' in request.form and request.method == 'POST':
        comments.DeleteTeam(request.form['deleteComment'])

    Simply if the user is the creator of that comment the key comes as a hidden input. And the buttons will be shown users which are for deletion operations.

    After those checks, comments are removed with the given key as hidden input.

    -Updating a PersonComment

    .. code-block:: python

        if request and 'updateComment' in request.form and request.method == 'POST':
            selectedComment = request.form['updateId']
            updatedComment = request.form['updateComment']
            comments.UpdatePersonComment(selectedComment, updatedComment)

    If the user is the creator of the comment, he/she can see the update button and key is came as hidden input.

    And user enters new comment, that comes with html requests and used for updating a tuble in the database.

    -Getting the PersonComments

    .. code-block:: python

        def personal_default_page_config(request):
            personComments = comments.GetPersonCommentsByCommentedPersonId(Current_Person[0])
            return render_template('personal/default.html', current_time=now.ctime(), Current_Person=Current_Person,
                           listFollowing=listFollowing, listFollowers=listFollowers, followed_projects=followed_projects,
                           personComments=personComments, listAccount=listAccount, listTitle=listTitle,
                           active_projects=active_projects, active_project_number=active_project_number,listEducation=listEducation, listSkill=listSkill,
                           listExperience=listExperience, listLanguage=listLanguage, listInformation=listInformation)


    Since comments are written to the user profile page, GetPersonCommentsByCommentedPersonId function only takes current person as parameter.

    After that since the URL should not be changed, render_template function is called accordingly.


****
Team
****

Table
-----

Team table exists in server.py file.

ObjectId attribute holds the primary key of the Team table.

ProjectId is the foreign key connected to Project.ObjectId

MemberId is also the foreign key connected to Person.ObjectId

.. code-block:: python

    CREATE TABLE IF NOT EXISTS Team(
           ObjectId SERIAL PRIMARY KEY,
           MemberId INTEGER NOT NULL,
           ProjectId INTEGER NOT NULL,
           Duty VARCHAR(500) NOT NULL,
           Deleted BOOLEAN NOT NULL
     )


    cursor.execute("""ALTER TABLE Team ADD  FOREIGN KEY(MemberId) REFERENCES Person(ObjectId) ON DELETE CASCADE""")
    cursor.execute("""ALTER TABLE Team ADD FOREIGN KEY(ProjectId) REFERENCES Project(ObjectId) ON DELETE CASCADE""")



Class
-----

Team class exists in team.py file which is in **classes** folder.

.. code-block:: python

    class Team:
        def __init__(self, objectId, projectId, memberId, duty):
            self.ObjectId = objectId
            self.MemberId = memberId
            self.ProjectId = projectId
            self.Duty = duty
            self.Deleted = 0

Class Operations
----------------
Team's class operations exists in information_operations.py which is in **classes/operations** folder.

- The following database operations are implemented for Information:
    -Add Operation

    .. code-block:: python

        def AddTeam(self, projectId, memberId, duty):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "INSERT INTO Team (MemberId, ProjectId, Duty, Deleted) VALUES (%s, %s, %s, False)"
                cursor.execute(query, (memberId, projectId, duty))
                connection.commit()
                self.last_key = cursor.lastrowid

    AddTeam takes the id's form interface and duty drom the user and inserts the new tuple composed of these values.

    -Delete Operation

    .. code-block:: python


        def DeleteTeam(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """DELETE FROM Team WHERE (ObjectId=%s)"""
                cursor.execute(query, (key,))
                connection.commit()

    DeleteTeam takes a key value which is the ObjectId of the Team to be deleted and removes the member from Team table.

    -Update Operation

    .. code-block:: python

       def UpdateMemberDuty(self, key, duty ):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """UPDATE Team SET Duty = %s WHERE (ObjectId=%s)""",
                    (duty, key))
                connection.commit()

    UpdateMemberDuty updates only the duty of the member in project selected by key which is given in interface.

    -Get Operation

    .. code-block:: python

        # Returns project name, person's duty in the project selected by person's name
        def GetAllTeamsByMemberId(self, personName):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT Project.Name, Team.Duty, Person.Name FROM Team
                           INNER JOIN Project ON(Team.ProjectId = Project.ObjectId)
                           INNER JOIN Person ON (Team.MemberId = Person.ObjectId)
                           WHERE (Person.Name = %s)"""
                cursor.execute(query, (personName,))
                result = cursor.fetchall()
            return result

        # Returns all team members in a project
        def GetAllMembersByProjectId(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT Person.FirstName ||' '|| Person.LastName as PersonFullName, Person.PhotoPath, Team.Duty, Person.ObjectId, Team.ObjectId
                           FROM Team
                           INNER JOIN Project ON(Team.ProjectId = Project.ObjectId)
                           INNER JOIN Person ON (Team.MemberId = Person.ObjectId)
                           WHERE (Team.ProjectId = %s) ORDER BY PersonFullName"""
                cursor.execute(query, (key,))
                result = cursor.fetchall()
            return result

        def GetDutyByMemberId(self, memberId, projectId):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT Duty FROM TEAM WHERE (MemberId=%s AND ProjectId=%s)"""
                cursor.execute(query, (memberId, projectId))
                result = cursor.fetchall()
            return result

Those operations are used for taking the tuple arrays and showing the updated records in each time after a database operation.

    - Count Operation

    .. code-block:: python

        def CountOfTeamsInProject(self, projectId):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT COUNT(*) FROM Team WHERE ProjectId=%s""", (projectId,))
                result = cursor.fetchone()
            return result

This function is used for gettting the number of members in a team. Since each project has a member limit, new members will not be added after the limit.

With this function the count of member number is gotten and used for comparison with a limit.


Templates
---------

project_html.html is the related template tfor Team Table in **templates/projects** folder.

GET/POST Operations
-------------------

    -Adding a Member

    .. code-block:: python

        elif 'addMember' in request.form:
            teamMembers = request.form.getlist('teamMember')
            lengthOfLoop = len(teamMembers)
            howManyMembers = teamList.CountOfTeamsInProject(key)
            projectTeamMembers = howManyMembers[0]
            for x in range(0, lengthOfLoop):
                if projectTeamMembers >= memberLimit:
                    break
                newMemberDuty = request.form['addDuty']
                newMemberMemberId = teamMembers[x]
                newMemberProjectId = key
                triedMember = teamList.GetDutyByMemberId(newMemberMemberId, key)
                lengthOfTried = len(triedMember)
                if lengthOfTried == 0:
                    projectTeamMembers +=1
                    teamList.AddTeam(newMemberProjectId, newMemberMemberId, newMemberDuty)
            return redirect(url_for('site.projects_details_page', key=key))

    Adding a new member and checking the project limit is done here in the for loop. memberLimit value is given from project table with a simple function.

    - Deleting a Member

    .. code-block:: python

        elif 'deleteMember' in request.form:
            deleteMemberId = request.form['deleteMember']
            teamList.DeleteTeam(deleteMemberId)
            return redirect(url_for('site.projects_details_page', key=key))

    The key of the function is given from interface and sent to delete function correspondingly.

    -Updating a Member

    .. code-block:: python

        elif 'updateMember' in request.form:
            newDuty = request.form['updatedMemberDuty']
            objectId = request.form['updatedMemberId']
            teamList.UpdateMemberDuty(objectId, newDuty)
            return redirect(url_for('site.projects_details_page', key=key))

    Here, updateMemberId came from the interface and updatedMemberDuty is written from user and Database table tuple is changed accordingly

    -Getting the Member/Members

    .. code-block:: python

        def project_details_page_config(submit_type, key):
            teamList = team_operations()
            necessaryProject = store.get_project_member_limit(key)
            memberLimit = necessaryProject[0][0]
            members = teamList.GetAllMembersByProjectId(key)
            return render_template('projects/project_details.html', project=project, project_comments=project_comments,
                               members=members, worklogs=worklogs, listManager=listManager, isFollow=isFollow,
                               current_user_objectid=current_user_objectid, project_creator=project_creator, listPerson=listPerson)

    If no parameter is given from HTML that function returns with the result of tuples.


******
Others
******

**In this page, functions which have common necessities by all members and implemented by Mehmet Barış Yaman are introduced.**

    .. code-block:: python

        def get_project_member_limit(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT MemberLimit FROM Project WHERE (ObjectId=%s)""", (key,))
                projects = cursor.fetchall()
                connection.commit()
            return projects

    This function is used to obtain the member limit of a project used in order to check that whether the project passes the member limit or not.

    .. code-block:: python

        def getUser(userEMail):
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                query = """SELECT Password FROM Users WHERE eMail = %s AND deleted='0'"""
                cursor.execute(query, (userEMail,))
                user_value = cursor.fetchone()
                if user_value is None:
                    return None
                password = user_value[0]
                user = User(userEMail, password)
            return user

    This function returns the user from the email given in login page.

    .. code-block:: python

        @app.route('/login', methods=["GET", "POST"])
        def login_page():
            if request.method == 'GET':
                comment = 'Sign in to start your AcademicFreelance life!'
                return render_template('login.html', comment=comment, person='asd')
            else:
                if 'login' in request.form:
                    email = request.form['email']
                    user = getUser(email)
                    if user is not None:
                        password = request.form['password']
                        if pwd_context.verify(password, user.password):
                            login_user(user)
                            next_page = request.args.get('next', url_for('site.home_page'))

                            return redirect(next_page)
                        else:
                            comment = 'Incorrect password. Please try again!'
                            return render_template('login.html', comment=comment)
                    else:
                        comment = 'No email is found. Please try again or register!'
                        return render_template('login.html', comment=comment)
                comment = 'Sign in to start your AcademicFreelance life!'
                return render_template('login.html', comment=comment)

    Login page operations are adjusted in server.py. Checking the passwords, showing the error messages in login operation is managed with that function.


    .. code-block:: python

        @site.route('/logout')
        @login_required
        def logout_page():
            flask_login.logout_user()
            return redirect(url_for('site.login_page'))

    Written in handlers.py for logout operation.


