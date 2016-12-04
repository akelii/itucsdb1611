from classes.education import Education
import psycopg2 as dbapi2
import datetime
from classes.model_config import dsn
class education_operations:
    def __init__(self):
        self.last_key=None

    def AddEducation(self, education):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Education (CVId, SchoolName, Description, GraduationGrade, StartDate, EndDate, Deleted) VALUES (%s, %s, %s, %s, %s, %s, FALSE )"
            cursor.execute(query, (education.CVId, education.SchoolName, education.Description, education.GraduationGrade, education.StartDate, education.EndDate))
            connection.commit()
            self.last_key = cursor.lastrowid

    def GetEducationListByCVId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Education.ObjectId, SchoolName, Description, GraduationGrade, StartDate, EndDate
                        FROM Education
                        INNER JOIN CV ON (Education.CVId = CV.ObjectId)
                        WHERE (Education.CVId=%s) ORDER BY Education.SchoolName DESC """
            cursor.execute(query, (key,))
            connection.commit()
            result = cursor.fetchall()
        return result

    def UpdateEducation(self, key, schoolname, description, grade, startdate, enddate):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE Education SET SchoolName = %s, Description = %s, GraduationGrade = %s, StartDate = %s, EndDate = %s WHERE (ObjectId=%s)""",
                (schoolname, description, grade, startdate, enddate, key))
            connection.commit()

    def DeleteEducation(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE Education SET Deleted = True WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()

    def DeleteEducationWithoutStore(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM Education WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()
