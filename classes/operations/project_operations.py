

import psycopg2 as dbapi2
from classes.followed_person import FollowedPerson
import datetime
from classes.model_config import dsn

class project_operations:
    def __init__(self):
        self.last_key = None


    def add_project(self, Project):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Project(Name, Description, ProjectTypeId, ProjectThesisTypeId, DepartmentId, ProjectStatusTypeId, StartDate, EndDate, MemberLimit, CreatedByPersonId, ProjectManagerId, Deleted) VALUES (%s, %s, %s, %s, %s, %s, ' "+str(datetime.datetime.now())+" ', %s, %s, %s, %s, False )",
                (Project.title, Project.project_description, Project.project_type, Project.project_thesis_type,
                 Project.department, Project.project_status_type, Project.end_date,
                 Project.member_limit, Project.created_by, Project.manager))
            connection.commit()
            self.last_key = cursor.lastrowid

    def delete_project(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM Project WHERE (ObjectId=%s)""", (key,))
            connection.commit()

    def update_project(self, key, title, project_description, end_date, member_limit, manager, deleted):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE Project SET Name = %s, Description = %s, EndDate = %s, MemberLimit = %s, ProjectManagerId = %s, Deleted = %s WHERE (ObjectId=%s)""",
                (title, project_description, end_date, member_limit, manager, deleted, key))
            connection.commit()

    def get_project(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Project.Name, Project.Description, ProjectType.Name, Department.Name, ProjectStatusType.Name, Person.FirstName, Person.LastName, Project.ObjectId FROM Project
                              JOIN ProjectType ON(Project.ProjectTypeId=ProjectType.ObjectId)
                              JOIN Department ON(Project.DepartmentId = Department.ObjectId)
                              JOIN ProjectStatusType ON(Project.ProjectStatusTypeId=ProjectStatusType.ObjectId)
                              JOIN Person ON(Project.CreatedByPersonId=Person.ObjectId)
                              WHERE (Project.ObjectID = %s)"""
            cursor.execute(query, (key,))
            project = cursor.fetchone()
            connection.commit()
        return project

    def get_projects(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT Project.ObjectId, Project.Name, Description, Department.Name
                              FROM Project JOIN Department ON(Project.DepartmentId = Department.ObjectId)""")
            projects = cursor.fetchall()
            connection.commit()
        return projects
