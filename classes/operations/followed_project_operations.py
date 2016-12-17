import psycopg2 as dbapi2
from classes.followed_project import FollowedProject
import datetime
from classes.model_config import dsn


class followed_project_operations:
    def __init__(self):
        self.last_key = None

    def AddFollowedProject(self, followed_project):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO FollowedProject (PersonId, FollowedProjectId, StartDate, Deleted) VALUES (%s, %s,' "+str(datetime.datetime.now())+"', False)"
            cursor.execute(query, (followed_project.PersonId, followed_project.FollowedProjectId))
            connection.commit()
            self.last_key = cursor.lastrowid

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

    def GetFollowedProjectList(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedProject.ObjectId, PersonId, ProjectTypeId, p2.Name as ProjectType,
                        Description, FollowedProjectId, p1.Name as FollowedProjectName, FollowedProject.StartDate
                        FROM FollowedProject
                        INNER JOIN Project as p1 ON p1.ObjectId = FollowedProject.FollowedProjectId
                        INNER JOIN  ProjectType p2 ON p2.ObjectId = p1.ProjectTypeId
                        WHERE (FollowedProject.Deleted='0') """
            cursor.execute(query)
            connection.commit()
            results = cursor.fetchall()
        return results

    # Belirtilen PersonId'ye sahip personın takip ettigi projeler
    def GetFollowedProjectListByPersonId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedProject.ObjectId, PersonId, ProjectTypeId, p2.Name as ProjectType,
                        Description, FollowedProjectId, p1.Name as FollowedProjectName, FollowedProject.StartDate
                        FROM FollowedProject
                        INNER JOIN Project as p1 ON p1.ObjectId = FollowedProject.FollowedProjectId
                        INNER JOIN  ProjectType p2 ON p2.ObjectId = p1.ProjectTypeId
                        WHERE (FollowedProject.PersonId = %s and FollowedProject.Deleted='0')"""
            cursor.execute(query, (key,))
            connection.commit()
            results = cursor.fetchall()
        return results

    # Belirtilen ProjectId'ye sahip projeyi takip eden personlar
    def GetFollowerPersonListByFollowedProjectId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedProject.ObjectId, PersonId, ProjectTypeId, p2.Name as ProjectType,
                        Description, FollowedProjectId, p1.Name as FollowedProjectName, FollowedProject.StartDate
                        FROM FollowedProject
                        INNER JOIN Project as p1 ON p1.ObjectId = FollowedProject.FollowedProjectId
                        INNER JOIN  ProjectType p2 ON p2.ObjectId = p1.ProjectTypeId
                        WHERE (FollowedProject.FollowedProjectId = %s and FollowedProject.Deleted='0')"""
            cursor.execute(query, (key,))
            connection.commit()
            results = cursor.fetchall()
        return results

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

    def DeleteFollowedProject(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM FollowedProject WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()

    def UpdateFollowedProject(self, key): #takip etmeye başlama zamanı update ediliyor, listede daha üstte görünecek
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE FollowedProject SET StartDate=' "+str(datetime.datetime.now())+"' WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()

