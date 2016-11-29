from classes.CV import CV
import psycopg2 as dbapi2
import datetime
from classes.model_config import dsn


class cv_operations:
    def __init__(self):
        self.last_key = None

    def get_cv(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM CV WHERE (ObjectID=%s)"
            cursor.execute(query, (key,))
            connection.commit()
            result = cursor.fetchone()
        return result

    def get_cvs(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT ObjectId, PersonId, CreatedDate, UpdatedDate, CvName FROM CV"
            cursor.execute(query)
            cvs = [(key, CV(key, PersonId, CreatedDate, UpdatedDate, CvName)) for
                   key, PersonId, CreatedDate, UpdatedDate, CvName in cursor]
        return cvs

    def update_cv(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "UPDATE CV SET UpdatedDate=NOW() WHERE ObjectId=(select cvid from education where objectid=%s)"
            key=str(key)
            cursor.execute(query, (key))
            connection.commit()


    def delete_cv(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM CV WHERE (ObjectId=%s)"
            cursor.execute(query, (key))
            connection.commit()
            cursor.close()


    def add_cv(self, cv,s1,s2):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO CV ( PersonId, CreatedDate, UpdatedDate, CvName, Deleted) VALUES (%s, %s, %s, %s,%s, 'FALSE')"
            cursor.execute(query, ('1',s1,s2,cv))
            connection.commit()
            self.last_key = cursor.lastrowid
        return cursor.lastrowid
