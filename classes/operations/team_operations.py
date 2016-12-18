import psycopg2 as dbapi2
from classes.team import Team
import datetime
from classes.model_config import dsn

class team_operations:
    def __init__(self):
        self.last_key=None

    def AddTeam(self, projectId, memberId, duty):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Team (MemberId, ProjectId, Duty, Deleted) VALUES (%s, %s, %s, False)"
            cursor.execute(query, (memberId, projectId, duty))
            connection.commit()
            self.last_key = cursor.lastrowid

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
                       WHERE (Team.ProjectId = %s) """
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

    def UpdateMemberDuty(self, key, duty ):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE Team SET Duty = %s WHERE (ObjectId=%s)""",
                (duty, key))
            connection.commit()


    def DeleteTeam(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM Team WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()

    def CountOfTeamsInProject(self, projectId):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT COUNT(*) FROM Team WHERE ProjectId=%s""", (projectId,))
            result = cursor.fetchone()
        return result


