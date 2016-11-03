

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
            query = """SELECT FollowedPerson.ObjectId ,PersonId ,p1.FirstName || ' ' || p1.LastName as PersonFullName
                       ,FollowedPersonId ,p2.FirstName || ' ' || p2.LastName as FollowedPersonFullName,StartDate
                       FROM FollowedPerson
                       INNER JOIN Person as p1 ON (FollowedPerson.PersonId = p1.ObjectId)
                       INNER JOIN Person as p2 ON (FollowedPerson.FollowedPersonId = p2.ObjectId)
                       WHERE (FollowedPerson.ObjectId=%s and FollowedPerson.Deleted='0')"""
            cursor.execute(query, (key,))
            result = cursor.fetchone()
        return result

    # Veritabanindaki butun elemanlari ceker
    def GetFollowedPersonList(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedPerson.ObjectId ,PersonId ,p1.FirstName || ' ' || p1.LastName as PersonFullName
                       ,FollowedPersonId ,p2.FirstName || ' ' || p2.LastName as FollowedPersonFullName,StartDate
                       FROM FollowedPerson
                       INNER JOIN Person as p1 ON (FollowedPerson.PersonId = p1.ObjectId)
                       INNER JOIN Person as p2 ON (FollowedPerson.FollowedPersonId = p2.ObjectId)
                       WHERE FollowedPerson.Deleted = '0' """
            cursor.execute(query)
            data_array = []
            results = cursor.fetchall()
            for followed_person in results:
                data_array.append(
                    {
                        'ObjectId': followed_person[0],
                        'PersonId': followed_person[1],
                        'PersonFullName': followed_person[2],
                        'FollowedPersonId': followed_person[3],
                        'FollowedPersonFullName': followed_person[4],
                        'StartDate': followed_person[5]
                    }
                )
        return results

    # Belirtilen PersonId'nin takip ettigi butun insanlari ceker
    def GetFollowedPersonListByPersonId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedPerson.ObjectId, PersonId, p1.FirstName || ' ' || p1.LastName as PersonFullName,
                        FollowedPersonId, p2.FirstName || ' ' || p2.LastName as FollowedPersonFullName,StartDate
                        FROM FollowedPerson
                        INNER JOIN Person as p1 ON p1.ObjectId = FollowedPerson.PersonId
                        INNER JOIN Person as p2 ON p2.ObjectId = FollowedPerson.FollowedPersonId
                        WHERE FollowedPerson.PersonId = %s"""
            cursor.execute(query, (key,))
            connection.commit()
            data_array = []
            results = cursor.fetchall()
            for followed_person in results:
                data_array.append(
                    {
                        'ObjectId': followed_person[0],
                        'PersonId': followed_person[1],
                        'PersonFullName': followed_person[2],
                        'FollowedPersonId': followed_person[3],
                        'FollowedPersonFullName': followed_person[4],
                        'StartDate': followed_person[5]
                    }
                )
        return results

    # Belirtilen FollowedPersonId'yi takip eden butun insanlari ceker
    def GetFollowedPersonListByFollowedPersonId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedPerson.ObjectId, PersonId, p1.FirstName || ' ' || p1.LastName as PersonFullName,
                        FollowedPersonId, p2.FirstName || ' ' || p2.LastName as FollowedPersonFullName,StartDate
                        FROM FollowedPerson
                        INNER JOIN Person as p1 ON p1.ObjectId = FollowedPerson.PersonId
                        INNER JOIN Person as p2 ON p2.ObjectId = FollowedPerson.FollowedPersonId
                        WHERE FollowedPerson.FollowedPersonId = %s"""
            cursor.execute(query, (key,))
            connection.commit()
            data_array = []
            results = cursor.fetchall()
            for followed_person in results:
                data_array.append(
                    {
                        'ObjectId': followed_person[0],
                        'PersonId': followed_person[1],
                        'PersonFullName': followed_person[2],
                        'FollowedPersonId': followed_person[3],
                        'FollowedPersonFullName': followed_person[4],
                        'StartDate': followed_person[5]
                    }
                )
        return results

