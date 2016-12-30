Parts Implemented by Güllü Katık
================================

****************
Followed Project
****************

Table
-----

FollowedProject table exists in server.py file.

ObjectId attribute holds the primary key of the FollowedProject table.

    .. code-block:: sql

        CREATE TABLE IF NOT EXISTS FollowedProject(
                ObjectId SERIAL PRIMARY KEY,
                PersonId INT NOT NULL,
                FollowedProjectId INT NOT NULL,
                StartDate TIMESTAMP NOT NULL,
                Deleted BOOLEAN NOT NULL
        )

PersonId is the foreign key that is connected to Person.ObjectId

    .. code-block:: sql

        ALTER TABLE FollowedProject ADD  FOREIGN KEY(PersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE

FollowedProjectId is the foreign key that is connected to Project.ObjectId

    .. code-block:: sql

        ALTER TABLE FollowedProject ADD  FOREIGN KEY(FollowedProjectId) REFERENCES Project(ObjectId) ON DELETE CASCADE

Class
-----

FollowedProject class exists in followed_project.py file which is in **classes** folder.

    .. code-block:: python

        class FollowedProject:
        def __init__(self,  objectId, personId, followedProjectId, startDate, deleted):
            self.ObjectId = objectId
            self.PersonId = personId
            self.FollowedProjectId = followedProjectId
            self.StartDate = startDate
            self.Deleted = deleted

Class Operations
----------------

FollowedProject's class operations exists in followed_project_operations.py which is in **classes/operations** folder.

- The following database operations are implemented for FollowedProject:

    -Add Operation

    .. code-block:: python

        def AddFollowedProject(self, followed_project):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "INSERT INTO FollowedProject (PersonId, FollowedProjectId, StartDate, Deleted) VALUES (%s, %s,' "+str(datetime.datetime.now())+"', False)"
                cursor.execute(query, (followed_project.PersonId, followed_project.FollowedProjectId))
                connection.commit()
                self.last_key = cursor.lastrowid

    AddFollowedProject function takes a followed project as parameter and inserts it to FollowedProject table.

    -Delete Operation

    .. code-block:: python

        def DeleteFollowedProject(self, key):
            with dbapi2.connect(dsn) as connection:
                 cursor = connection.cursor()
                 query = """DELETE FROM FollowedProject WHERE (ObjectId=%s)"""
                 cursor.execute(query, (key,))
                 connection.commit()

    DeleteFollowedProject function takes a key as parameter and deletes followed project whose ObjectId is equal to key from FollowedProject table.

    -Update Operation

    .. code-block:: python

        def UpdateFollowedProject(self, key):
            with dbapi2.connect(dsn) as connection:
                 cursor = connection.cursor()
                 query = """UPDATE FollowedProject SET StartDate=' "+str(datetime.datetime.now())+"' WHERE (ObjectId=%s)"""
                 cursor.execute(query, (key,))
                 connection.commit()

    UpdateFollowedProject function takes a key as parameter and updates SatartDate of followed project whose ObjectId is equal to key.

    -Get Operations

    .. code-block:: python

        def GetFollowedProjectByObjectId(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT FollowedProject.ObjectId, PersonId, ProjectTypeId, p2.Name as ProjectType,
                            Description, FollowedProjectId, p1.Name as FollowedProjectName, FollowedProject.StartDate
                            FROM FollowedProject
                            INNER JOIN Project as p1 ON p1.ObjectId = FollowedProject.FollowedProjectId
                            INNER JOIN  ProjectType p2 ON p2.ObjectId = p1.ProjectTypeId
                            WHERE (FollowedProject.ObjectId=%s and FollowedProject.Deleted='0')"""
                cursor.execute(query, (key,))
                result = cursor.fetchone()
            return result

    GetFollowedProjectByObjectId takes a key value as parameter and returns the followed project which has the same ObjectId with the key.

    .. code-block:: python

        def GetFollowedProjectListByPersonId(self, key):
            with dbapi2.connect(dsn) as connection:
                 cursor = connection.cursor()
                 query = """SELECT FollowedProject.ObjectId, PersonId, ProjectTypeId, p2.Name as ProjectType,
                            Description, FollowedProjectId, p1.Name as FollowedProjectName, FollowedProject.StartDate, p1.ObjectId
                            FROM FollowedProject
                            INNER JOIN Project as p1 ON p1.ObjectId = FollowedProject.FollowedProjectId
                            INNER JOIN  ProjectType p2 ON p2.ObjectId = p1.ProjectTypeId
                            WHERE (FollowedProject.PersonId = %s and FollowedProject.Deleted='0')"""
                 cursor.execute(query, (key,))
                 connection.commit()
                 results = cursor.fetchall()
            return results

    GetFollowedProjectListByPersonId takes a key value as parameter and returns the followed projects which has the same FollowedProject.PersonId with the key.

    .. code-block:: python

        def GetFollowedProjectByPersonIdAndProjectId(self, personId, projectId):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT FollowedProject.ObjectId, PersonId, ProjectTypeId, p2.Name as ProjectType,
                            Description, FollowedProjectId, p1.Name as FollowedProjectName, FollowedProject.StartDate
                            FROM FollowedProject
                            INNER JOIN Project as p1 ON p1.ObjectId = FollowedProject.FollowedProjectId
                            INNER JOIN  ProjectType p2 ON p2.ObjectId = p1.ProjectTypeId
                            WHERE (FollowedProject.FollowedProjectId = %s and FollowedProject.PersonId = %s and FollowedProject.Deleted='0')"""
                cursor.execute(query, (projectId, personId))
                result = cursor.fetchone()
            return result

    GetFollowedProjectByPersonIdAndProjectId takes personId and projectId as parameters and returns the followed project which has the same FollowedProject.PersonId with the personId and has the same FollowedProject.FollowedProjectId with the projectId.

Templates
---------
**person_detail.html**, **default.html**, **project_details.html**, and **search_project.html** are the related templates to FollowedProject.

GET/POST Operations
-------------------

    -Adding a FollowedProject

    -On project details page

    .. code-block:: python

        elif 'follow' in request.form:
            follow_project = FollowedProject(None, current_person[0], key, ' "+str(datetime.datetime.now())+" ', False)
            followed_projects.AddFollowedProject(follow_project)
            return redirect(url_for('site.projects_details_page', key=key))

    When the user click follow button on project details page, an followed project object is created. This objects PersonId is current users ObjectId and its FollowedProjectId is key. Then AddFollowedProject function takes that object as parameter and adds the project to followed projects

    -On search project page

    .. code-block:: python

        elif 'follow' in request.form:
            project_id = request.form['follow']
            followProject = FollowedProject(None, currentUser[0], project_id,'"+str(datetime.datetime.now())+"', False)
            store_followed.AddFollowedProject(followProject)
            return redirect(url_for('site.projects_search_page'))

    In this case ProjectId is taken from the form

    -Deleting a FollowedProject

    -On project details page

    .. code-block:: python

        elif 'unfollow' in request.form:
            unfollow_project_id = followed_projects.GetFollowedProjectByPersonIdAndProjectId(current_person[0] ,key)[0]
            followed_projects.DeleteFollowedProject(unfollow_project_id)
            return redirect(url_for('site.projects_details_page', key=key))

    To get ObjectId of the followed project to be deleted call GetFollowedProjectByPersonIdAndProjectId function with current persons ObjectId and projects ObjectId. Then the followed project is deleted from FolllowedProject table.

    -On search project page

    .. code-block:: python

        elif 'unfollow' in request.form:
            project_id = request.form['unfollow']
            delete_project = store_followed.GetFollowedProjectByPersonIdAndProjectId(currentUser[0], project_id)
            store_followed.DeleteFollowedProject(delete_project[0])
            return redirect(url_for('site.projects_search_page'))

    In this case ProjectId is taken from the form

    -Getting Followed Projects

    .. code-block:: python

        def personal_default_page_config(request):
            PersonProvider = person_operations()
            Current_Person = PersonProvider.GetPerson(current_user.email)
            store_followed_projects = followed_project_operations()
            followed_projects = store_followed_projects.GetFollowedProjectListByPersonId(Current_Person[0])
            return render_template('personal/default.html', current_time=now.ctime(), Current_Person=Current_Person,
                           listFollowing=listFollowing, listFollowers=listFollowers, followed_projects=followed_projects,
                           personComments=personComments, listAccount=listAccount, listTitle=listTitle,
                           active_projects=active_projects, active_project_number=active_project_number,listEducation=listEducation, listSkill=listSkill,
                           listExperience=listExperience, listLanguage=listLanguage, listInformation=listInformation)


*******
Worklog
*******

Table
-----

Worklog table exists in server.py file.

ObjectId attribute holds the primary key of the Worklog table.

    .. code-block:: sql

        CREATE TABLE IF NOT EXISTS WorkLog (
                ObjectId SERIAL PRIMARY KEY,
                ProjectId INTEGER NOT NULL,
                CommitMessage VARCHAR(500) NOT NULL,
                CreatedDate TIMESTAMP NOT NULL,
                CreatorPersonId INTEGER NOT NULL,
                Deleted BOOLEAN NOT NULL
        )

ProjectId is the foreign key that is connected to Project.ObjectId

    .. code-block:: sql

        ALTER TABLE Worklog ADD  FOREIGN KEY(CreatorPersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE

CreatorPersonId is the foreign key that is connected to Person.ObjectId

    .. code-block:: sql

        ALTER TABLE Worklog ADD  FOREIGN KEY(ProjectId) REFERENCES Project(ObjectId) ON DELETE CASCADE

Class
-----

Worklog class exists in work_log.py file which is in **classes** folder.

    .. code-block:: python

        class WorkLog:
            def __init__(self, objectId, projectId, commitMessage, createDate, creatorPersonId, deleted):
                self.ObjectId = objectId
                self.ProjectId = projectId
                self.CommitMessage = commitMessage
                self.CreateDate = createDate
                self.CreatorPersonId = creatorPersonId
                self.Deleted = deleted

Class Operations
----------------

Worklog's class operations exists in work_log_operations.py which is in **classes/operations** folder.

- The following database operations are implemented for Worklog:

    -Add Operation

    .. code-block:: python

        def AddWorkLog(self, work_log):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "INSERT INTO WorkLog (ProjectId, CommitMessage, CreatedDate, CreatorPersonId, Deleted) VALUES (%s, %s,' "+str(datetime.datetime.now())+" ', %s, False)"
                cursor.execute(query, (work_log.ProjectId, work_log.CommitMessage, work_log.CreatorPersonId))
                connection.commit()
                self.last_key = cursor.lastrowid

    AddWorkLog function takes a work log as parameter and inserts it to Worklog table.

    -Delete Operation

    .. code-block:: python

        def DeleteWorkLog(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """DELETE FROM WorkLog WHERE (ObjectId=%s)"""
                cursor.execute(query, (key,))
                connection.commit()

    DeleteWorkLog function takes a key as parameter and deletes work log whose ObjectId is equal to key from Worklog table.

    -Update Operation

    .. code-block:: python

        def UpdateWorkLog(self, key, commitMessage):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """UPDATE Worklog SET CommitMessage = %s WHERE (ObjectId = %s)"""
                cursor.execute(query, (commitMessage, key,))
                connection.commit()

    UpdateFollowedProject function takes a key and commitMessage as parameters and updates CommitMessage of work log whose ObjectId is equal to key.

    -Get Operations

    .. code-block:: python

        def GetWorkLogByProjectId(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT WorkLog.ObjectId, CommitMessage, CreatedDate, CreatorPersonId ,p1.FirstName || ' ' || p1.LastName as CreatorPersonName,
                                              ProjectId, p2.Name as ProjectName
                                              FROM WorkLog
                                              INNER JOIN Person as p1 ON (WorkLog.CreatorPersonId = p1.ObjectId)
                                              INNER JOIN Project as p2 ON (WorkLog.ProjectId = p2.ObjectId)
                                              WHERE (WorkLog.ProjectId=%s and Worklog.Deleted='0') ORDER BY WorkLog.CreatedDate DESC"""
                cursor.execute(query, (key,))
                connection.commit()
                results = cursor.fetchall()
            return results

    GetWorkLogByProjectId takes a key value as parameter and returns the work logs which has the same ProjectId with the key.

    -Get Operations

    .. code-block:: python

        def GetFollowedProjectsWorkLogs(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT WorkLog.ObjectId, CommitMessage, CreatedDate, CreatorPersonId ,p1.FirstName || ' ' || p1.LastName as CreatorPersonName,
                                              ProjectId, p2.Name as ProjectName
                                              FROM WorkLog
                                              INNER JOIN Person as p1 ON (WorkLog.CreatorPersonId = p1.ObjectId)
                                              INNER JOIN Project as p2 ON (WorkLog.ProjectId = p2.ObjectId)
                                              JOIN FollowedProject as p3 ON (WorkLog.ProjectId = p3.FollowedProjectId)
                                              WHERE (p3.PersonId = %s
                                              AND Worklog.Deleted='0') ORDER BY WorkLog.CreatedDate DESC """
                cursor.execute(query, (key,))
                connection.commit()
                results = cursor.fetchall()
            return results

    GetFollowedProjectWorkLogs takes a key value as parameter and returns the work logs of projects that in the FollowedProject table.

Templates
---------
**project_details.html**, and **dashboard.html** are the related templates to Worklog.

GET/POST Operations
-------------------

    -Adding a Worklog

    .. code-block:: python

        elif 'addWorklog' in request.form:
            cretaorPersonId = person_operations.GetPerson(current_user, current_user.email)[0]
            projectId = key
            commitMessage = request.form['commitMessage']
            worklog = WorkLog(None, projectId, commitMessage, ' "+str(datetime.datetime.now())+" ', cretaorPersonId, False)
            store_worklogs.AddWorkLog(worklog)
            return redirect(url_for('site.projects_details_page', key=key))

    CreatorPersonId of new work log is current users ObjectId

    CommitMessage is taken from form(user)

    ProjectId is key

    A work log object is created by using this parameters and is added to the projects work logs

    -Deleting a Worklog

    .. code-block:: python

        elif 'deleteWorklog' in request.form:
            worklog_id = request.form['deleteWorklog']
            store_worklogs.DeleteWorkLog(worklog_id)
            return redirect(url_for('site.projects_details_page', key=key))

    -Updating Worklog

    .. code-block:: python

        elif 'editWorklog' in request.form:
            worklog_id = request.form['editWorklog']
            new_log = request.form['new_log']
            store_worklogs.UpdateWorkLog(worklog_id, new_log)
            return redirect(url_for('site.projects_details_page', key=key))

     -Getting Worklogs

    -On projects details page

    .. code-block:: python

        store_worklogs = work_log_operations()
        if submit_type == 'GET':
            worklogs = store_worklogs.GetWorkLogByProjectId(key)
            current_user_objectid = person_operations.GetPerson(current_user, current_user.email)[0]
            return render_template('projects/project_details.html', project=project, project_comments=project_comments,
                                   members=members, worklogs=worklogs, listManager=listManager, isFollow=isFollow,
                                   current_user_objectid=current_user_objectid, project_creator=project_creator, listPerson=listPerson)

    -On home page

    .. code-block:: python

    def home_page_config(request):
        PersonProvider = person_operations()
        Current_Person = PersonProvider.GetPerson(current_user.email)
        store_worklogs = work_log_operations()
        worklogs = store_worklogs.GetFollowedProjectsWorkLogs(Current_Person[0])
        return render_template('dashboard.html', worklogs=worklogs, active_projects=active_projects)

*****
Skill
*****

Table
-----

Skill table exists in server.py file.

ObjectId attribute holds the primary key of the Skill table.

    .. code-block:: sql

        CREATE TABLE IF NOT EXISTS Skill(
                ObjectId SERIAL PRIMARY KEY,
                CVId INTEGER NOT NULL,
                Name VARCHAR(50) NOT NULL,
                Level VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )

CVId is the foreign key that is connected to CV.ObjectId

    .. code-block:: sql

        ALTER TABLE Skill ADD FOREIGN KEY(CVId) REFERENCES CV(ObjectId) ON DELETE CASCADE

Class
-----

Skill class exists in language.py file which is in **classes** folder.

.. code-block:: python

    class Skill:
        def __init__(self, objectId, cvId, name, level):
            self.ObjectId = objectId
            self.CVId = cvId
            self.Name = name
            self.Level = level
            self.Deleted = 0

Class Operations
----------------

Skill class operations exists in skill_operations.py which is in **classes/operations** folder.

- The following database operations are implemented for Skill Class:

    -Add Operation

    .. code-block:: python

        def AddSkill(self, cvId, name, level):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "INSERT INTO Skill(CVId, Name, Level, Deleted) VALUES(%s, %s, %s, FALSE)"
                cursor.execute(query, (cvId, name, level,))
                connection.commit()
                self.last_key = cursor.

    AddSkill takes skill's CV id, name and level as parameters and inserts the attributes to the Skill Table.

    -Delete Operation

    .. code-block:: python

        def DeleteSkill(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """DELETE FROM Skill WHERE(ObjectId = %s)"""
                cursor.execute(query, (key,))
                connection.commit()

    DeleteSkill function takes a key as parameter and deletes skill whose ObjectId is equal to key from Skill table.

    -Update Operation

    .. code-block:: python

        def UpdateSkill(self, key, name, level):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """UPDATE Skill SET Name = %s, Level = %s WHERE(ObjectId = %s)"""
                cursor.execute(query, (name, level, key,))
                connection.commit()

    UpdateSkill takes key value, name and level as parameters and updates the information whose ObjectId is the key, with the given attribute.

    -Get Operation

    .. code-block:: python

        def GetSkillByCVId(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = """SELECT ObjectId, CVId, Name, Level FROM Skill
                        WHERE CVId = %s"""
                cursor.execute(query, (key,))
                results = cursor.fetchall()
                return results

    GetSkillByCVId function takes a key value as parameter and returns related CV's skill, which has the same ObjectId with the key.

Templates
---------
**cv.html**, **person_detail.html** and **default.html** are the related templates to Skill.

GET/POST Operations
-------------------

    -Adding a Skill

    .. code-block:: python

        elif request and 'newSkill' in request.form and request.method == 'POST':
            newSkillName = request.form['newSkill']
            skillLevel = request.form['skillLevel']
            store_skill.AddSkill(key, newSkillName, skillLevel)
            skills = store_skill.GetSkillByCVId(key)
            updateCV = "TRUE"

    -Deleting a Skill

    .. code-block:: python

        elif request and 'deleteSkill' in request.form and request.method == 'POST':
            delete_id = request.form['deleteSkill']
            store_skill.DeleteSkill(delete_id)
            skills = store_skill.GetSkillByCVId(key)
            updateCV = "TRUE"

    -Updating a Skill

    .. code-block:: python

        elif request and 'updateSkillName' in request.form and request.method == 'POST':
            updateSkillName = request.form['updateSkillName']
            updateSkillLevel = request.form['updateSkillLevel']
            update_id = request.form['updateSkillId']
            store_skill.UpdateSkill(update_id, updateSkillName, updateSkillLevel)
            skills = store_skill.GetSkillByCVId(key)
            updateCV = "TRUE"


    -Getting Skills

    .. code-block:: python

        def personal_cv_pagewithkey_config(submit_type, key):
            PersonProvider = person_operations()
            CurrentPerson = PersonProvider.GetPerson(current_user.email)
            store_skill = skill_operations()
            skills = store_skill.GetSkillByCVId(key)
            return render_template('personal/cv.html', cvs=cvs,CurrentCV=CurrentCV, languages = allLanguages, experiences=experiences, listEducation=listEducation,
                                   current_time=now.ctime(), informationn=allInformation, listInformation=listInformation, skills=skills)



    All skills belong to the CV are gotten and they are shown on CV page.
