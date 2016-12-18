import psycopg2 as dbapi2
from classes.work_log import  WorkLog
import datetime
from classes.model_config import dsn


class work_log_operations:
    def __init__(self):
        self.last_key = None

    def AddWorkLog(self, work_log):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO WorkLog (ProjectId, CommitMessage, CreatedDate, CreatorPersonId, Deleted) VALUES (%s, %s,' "+str(datetime.datetime.now())+" ', %s, False)"
            cursor.execute(query, (work_log.ProjectId, work_log.CommitMessage, work_log.CreatorPersonId))
            connection.commit()
            self.last_key = cursor.lastrowid

    def GetWorkLogByObjectId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT WorkLog.ObjectId, CommitMessage, CreatedDate, CreatorPersonId ,p1.FirstName || ' ' || p1.LastName as CreatorPersonName,
                                   ProjectId, p2.Name as ProjectName
                                   FROM WorkLog
                                   INNER JOIN Person as p1 ON (WorkLog.CreatorPersonId = p1.ObjectId)
                                   INNER JOIN Project as p2 ON (WorkLog.ProjectId = p2.ObjectId)
                                   WHERE (WorkLog.ObjectId=%s and Worklog.Deleted='0')"""
            cursor.execute(query, (key,))
            connection.commit()
            result = cursor.fetchone()
        return result

    def GetAllWorkLogs(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT WorkLog.ObjectId, CommitMessage, CreatedDate, CreatorPersonId ,p1.FirstName || ' ' || p1.LastName as CreatorPersonName,
                                          ProjectId, p2.Name as ProjectName
                                          FROM WorkLog
                                          INNER JOIN Person as p1 ON (WorkLog.CreatorPersonId = p1.ObjectId)
                                          INNER JOIN Project as p2 ON (WorkLog.ProjectId = p2.ObjectId)
                                          WHERE Worklog.Deleted='0' ORDER BY WorkLog.CreatedDate DESC"""
            cursor.execute(query)
            connection.commit()
            results = cursor.fetchall()
        return results

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

    def GetFollowedProjectsWorkLogs(self, key): #takip edilen projelerin loglarını dashboardda göstermek için
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

    def UpdateWorkLog(self, key, commitMessage):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE Worklog SET CommitMessage = %s WHERE (ObjectId = %s)"""
            cursor.execute(query, (commitMessage, key,))
            connection.commit()

    def DeleteWorkLog(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM WorkLog WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()