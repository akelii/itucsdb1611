from classes.CV import CV
import psycopg2 as dbapi2
import datetime
from classes.model_config import dsn
from classes.operations.person_operations import person_operations

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
          #  if type == 'e':
            query = "UPDATE CV SET UpdatedDate=NOW() WHERE( ObjectId=%s)"
           # elif type=='l':
            #    query = "UPDATE CV SET UpdatedDate=NOW() WHERE ObjectId=(select cvid from language where objectid=%s)"
            #key=str(key)
            cursor.execute(query, (key,))
            connection.commit()


    def delete_cv(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM CV WHERE (ObjectId=%s)"
            cursor.execute(query, (str(key),))
            connection.commit()
            cursor.close()


    def add_cv_with_key(self, cvName,key):
        cvStore=cv_operations()
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            currentCV=cvStore.get_cv(key)
            query = "INSERT INTO CV ( PersonId, CreatedDate, UpdatedDate, CvName, Deleted) VALUES (%s, NOW(), NOW(), %s, 'FALSE')"
            cursor.execute(query, (currentCV[1],cvName,))
            connection.commit()
            self.last_key = cursor.lastrowid


    def add_cv(self, cvName):
        cvStore = cv_operations()
        personStore=person_operations()
        UserList=personStore.GetPersonList()
        randomUser=UserList[0]
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO CV ( PersonId, CreatedDate, UpdatedDate, CvName, Deleted) VALUES (%s, NOW(), NOW(), %s, 'FALSE')"
            cursor.execute(query, (randomUser[0], cvName))
            connection.commit()
            self.last_key = cursor.lastrowid
































