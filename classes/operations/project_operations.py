

import psycopg2 as dbapi2
import datetime
from classes.model_config import dsn

class project_operations:
    def __init__(self):
        self.last_key = None


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

    def get_projects(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT Project.ObjectId, Project.Name, Description, Department.Name, Person.FirstName, Person.LastName
                              FROM Project JOIN Department ON(Project.DepartmentId = Department.ObjectId) JOIN Person ON(Person.ObjectId = Project.ProjectManagerId)""")
            projects = cursor.fetchall()
            connection.commit()
        return projects

    def get_project_member_limit(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT MemberLimit FROM Project WHERE (ObjectId=%s)""", (key,))
            projects = cursor.fetchall()
            connection.commit()
        return projects

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


    def get_last(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT ObjectId FROM Project Order By ObjectId Desc LIMIT 1""")
            projectId = cursor.fetchone()
            connection.commit()
        return projectId

