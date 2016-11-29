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
                        WHERE (Education.CVId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()
            result = cursor.fetchall()
        return result
