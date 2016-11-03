

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

    def update_project(self, key, title, project_description, project_type, project_thesis_type, department,
                       project_status_type, start_date, end_date, member_limit, team, created_by, manager, deleted):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE Project SET Name = %s, Description = %s, ProjectTypeId = %s, ProjectThesisTypeId = %s, DepartmentId = %s, ProjectStatusTypeId = %s, StartDate = %s, EndDate = %s, MemberLimit = %s, TeamId = %s, CreatedByPersonId = %s, ProjectManagerId = %s, Deleted = %s WHERE (ObjectId=%s)""",
                (title, project_description, project_type, project_thesis_type, department, project_status_type,
                 start_date, end_date, member_limit, team, created_by, manager, deleted, key))
            connection.commit()

    def get_project(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT Name, Description FROM Project WHERE (ObjectID=%s)""", (key,))
            connection.commit()

    def get_projects(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM Project""")
            projects = cursor.fetchall()
            connection.commit()
        return projects
