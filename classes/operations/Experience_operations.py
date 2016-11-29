
import psycopg2 as dbapi2
from classes.Experience import Experience
from classes.model_config import dsn
from classes.CV import CV


class experience_operations:
    def __init__(self):
        self.last_key=None



    def get_experience(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT Description, CompanyName, ExperiencePosition, StartDate, EndDate FROM Experience WHERE (ObjectID=%s)"
            cursor.execute(query, (key))
            connection.commit()


    def update_experience(self, key, description, startDate, endDate, companyName, experiencePosition ):
        with dbapi2.connect(dsn) as connection:
            cursor =connection.cursor()
            query = "UPDATE Experience SET Description=%s, StartDate=%s, EndDate=%s, CompanyName=%s, ExperiencePosition=%s WHERE (ObjectId=%s)"
            cursor.execute(query, (description, startDate, endDate, companyName, experiencePosition,key))
            connection.commit()


    def delete_experience(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM Experience WHERE (ObjectId=%s)"
            cursor.execute(query, (key,) )
            connection.commit()
            cursor.close()



    def add_experience(self, CVId, Description, CompanyName, ExperiencePosition,StartDate,EndDate):
       with dbapi2.connect(dsn) as connection:
           cursor = connection.cursor()
           query = "INSERT INTO Experience (CVId, Description, CompanyName, ExperiencePosition, StartDate, EndDate, DELETED) VALUES (%s, %s, %s, %s, %s, %s, FALSE)"
           cursor.execute(query, ( CVId, Description,CompanyName, ExperiencePosition, StartDate, EndDate ))
           connection.commit()
           self.last_key = cursor.lastrowid
       return cursor.lastrowid


    def get_experience_s(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT ObjectId,CVId,Description, CompanyName, ExperiencePosition, StartDate, EndDate FROM Experience ORDER BY ObjectID"
            cursor.execute(query)
            experience_s=[(key, Experience( key, CVId, Description, CompanyName,   StartDate, EndDate,ExperiencePosition ))for key, CVId, Description, CompanyName,  StartDate,EndDate,ExperiencePosition in cursor]
        return experience_s