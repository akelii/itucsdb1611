

import psycopg2 as dbapi2
from classes.followed_person import FollowedPerson
import datetime
from classes.model_config import dsn

class followed_person_operations:
    def __init__(self):
        self.last_key=None

    def AddFollowedPerson(self, followed_person):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO FollowedPerson (PersonId, FollowedPersonId, StartDate, Deleted) VALUES (%s, %s,' "+str(datetime.datetime.now())+"', False)"
            cursor.execute(query, (followed_person.PersonId, followed_person.FollowedPersonId))
            connection.commit()
            self.last_key = cursor.lastrowid

    # ObjectId'ye gore bir eleman doner.
    def GetFollowedPersonByObjectId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT PersonId, FollowedPersonId, StartDate FROM FollowedPerson WHERE (ObjectId=%s and Deleted='0')"
            cursor.execute(query, (key,))
            result = cursor.fetchone()
        return result

    # Veritabanindaki deleted'ı true olmayan butun elemanlari ceker
    def GetFollowedPersonList(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT PersonId, FollowedPersonId, StartDate FROM FollowedPerson WHERE (Deleted='0')"
            cursor.execute(query)
            results = cursor.fetchall()
        return results

