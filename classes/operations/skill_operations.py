import psycopg2 as dbapi2
from classes.skill import Skill
import datetime
from classes.model_config import dsn

class skill_operations:
    def __init__(self):
        self.last_key = None

    def AddSkill(self, cvId, name, level):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Skill(CVId, Name, Level, Deleted) VALUES(%s, %s, %s, FALSE)"
            cursor.execute(query, (cvId, name, level,))
            connection.commit()
            self.last_key = cursor.lastrowid

    def GetSkillByCVId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT CVId ,Name, Level FROM Skill
                    WHERE CVId = %s"""
            cursor.execute(query, (key,))
            results = cursor.fetchall()
            return results

    def DeleteSkill(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM Skill WHERE(ObjectId = %s)"""
            cursor.execute(query, (key,))
            connection.commit()

    def UpdateSkill(self, key, name, level):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE Skill SET Name = %s, Level = %s WHERE(ObjectId = %s)"""
            cursor.execute(query, (name, level, key,))
            connection.commit()