

import psycopg2 as dbapi2
from classes.CVInformation import CVInformation
from classes.model_config import dsn
from classes.CV import CV


class cv_information_operations:
    def __init__(self):
        self.last_key=None



    def get_cv_information(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT Description , CVInformationTypeId FROM CVInformation WHERE (ObjectID=%s)"
            cursor.execute(query, (key))
            connection.commit()


    def update_cv_information(self, key, description, startDate, endDate ):
        with dbapi2.connect(dsn) as connection:
            cursor =connection.cursor()
            query = "UPDATE CVInformation SET Description=%s, StartDate=%s, EndDate=%s WHERE (ObjectId=%s)"
            cursor.execute(query, (description, startDate, endDate,key))
            connection.commit()


    def delete_cv_information(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM CVInformation WHERE (ObjectId=%s)"
            cursor.execute(query, (key,) )
            connection.commit()
            cursor.close()



    def add_cv_information(self, cvInfo):
       with dbapi2.connect(dsn) as connection:
           cursor = connection.cursor()
           query = "INSERT INTO CVInformation (CVId, Description, CVInformationTypeId, StartDate, EndDate, DELETED) VALUES (%s, %s, %s, %s, %s, FALSE)"
           cursor.execute(query, ( cvInfo.CVId, cvInfo.Description, cvInfo.CVInformationTypeId, cvInfo.StartDate, cvInfo.EndDate ))
           connection.commit()
           self.last_key = cursor.lastrowid
       return cursor.lastrowid


    def get_cv_information_s(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT ObjectId,CVId, Description, CVInformationTypeId , StartDate, EndDate FROM CVInformation ORDER BY ObjectID"
            cursor.execute(query)
            cv_information_s=[(key, CVInformation( key, CVId, Description, CVInformationTypeId,  StartDate, EndDate ))for key, CVId, Description, CVInformationTypeId, StartDate,EndDate in cursor]
        return  cv_information_s