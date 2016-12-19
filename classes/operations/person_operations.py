
from classes.person import Person
import psycopg2 as dbapi2
import datetime
from classes.model_config import dsn
class person_operations:
    def __init__(self):
        self.last_key=None

    def AddPerson(self, person):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Person (FirstName, LastName, AccountTypeId, Email, Password, Gender, TitleId, PhotoPath, Deleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE )"
            cursor.execute(query, (person.FirstName, person.LastName, person.AccountTypeId, person.Email, person.Password, person.Gender, person.TitleId, person.PhotoPath))
            connection.commit()
            self.last_key = cursor.lastrowid

    def GetPersonByObjectId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Person.ObjectId, FirstName || ' ' || LastName as FullName, AccountType.AccountTypeName, Email, Password, Gender, Title.Name, PhotoPath, FirstName, LastName
                        FROM Person
                        INNER JOIN AccountType ON (Person.AccountTypeId = AccountType.ObjectId)
                        INNER JOIN Title ON (Person.TitleId = Title.ObjectId)
                        WHERE (Person.ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()
            result = cursor.fetchone()
        return result

    def GetPerson(self, userEMail):#current_userın emaili ile person tablosundaki haline ulaşıyoruz
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Person.ObjectId, FirstName || ' ' || LastName as FullName, AccountType.AccountTypeName, Email, Password, Gender, Title.Name, PhotoPath, FirstName, LastName
                        FROM Person
                        INNER JOIN AccountType ON (Person.AccountTypeId = AccountType.ObjectId)
                        INNER JOIN Title ON (Person.TitleId = Title.ObjectId)
                        WHERE eMail = %s"""
            cursor.execute(query, (userEMail,))
            person_id = cursor.fetchone()
        return person_id

    def GetPersonList(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Person.ObjectId, FirstName || ' ' || LastName as FullName, AccountType.AccountTypeName, Email, Password, Gender, Title.Name, PhotoPath
                        FROM Person
                        INNER JOIN AccountType ON (Person.AccountTypeId = AccountType.ObjectId)
                        INNER JOIN Title ON (Person.TitleId = Title.ObjectId)
                        ORDER BY Person.ObjectId"""
            cursor.execute(query)
            connection.commit()
            data_array = []
            results = cursor.fetchall()
            for person in results:
                data_array.append(
                    {
                        'ObjectId': person[0],
                        'PersonFullName': person[1],
                        'AccountTypeName': person[2],
                        'eMail': person[3],
                        'Password': person[4],
                        'Gender': person[5],
                        'TitleName': person[6],
                        'PhotoPath': person[7]
                    }
                )
        return results


    def GetLastThreePeople(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Person.ObjectId, FirstName || ' ' || LastName as FullName, AccountType.AccountTypeName, Email, Password, Gender, Title.Name, PhotoPath
                        FROM Person
                        INNER JOIN AccountType ON (Person.AccountTypeId = AccountType.ObjectId)
                        INNER JOIN Title ON (Person.TitleId = Title.ObjectId)
                        ORDER BY Person.ObjectId DESC LIMIT 3"""
            cursor.execute(query)
            connection.commit()
            data_array = []
            results = cursor.fetchall()
            for person in results:
                data_array.append(
                    {
                        'ObjectId': person[0],
                        'PersonFullName': person[1],
                        'AccountTypeName': person[2],
                        'eMail': person[3],
                        'Password': person[4],
                        'Gender': person[5],
                        'TitleName': person[6],
                        'PhotoPath': person[7]
                    }
                )
        return results

    def GetPersonListExcludePersonId(self,key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Person.ObjectId, FirstName || ' ' || LastName as FullName, AccountType.AccountTypeName, Email, Password, Gender, Title.Name, PhotoPath
                        FROM Person
                        INNER JOIN AccountType ON (Person.AccountTypeId = AccountType.ObjectId)
                        INNER JOIN Title ON (Person.TitleId = Title.ObjectId)
                        WHERE (Person.ObjectId!=%s)
                        ORDER BY Person.FirstName"""
            cursor.execute(query, (key,))
            connection.commit()
            data_array = []
            results = cursor.fetchall()
            for person in results:
                data_array.append(
                    {
                        'ObjectId': person[0],
                        'PersonFullName': person[1],
                        'AccountTypeName': person[2],
                        'eMail': person[3],
                        'Password': person[4],
                        'Gender': person[5],
                        'TitleName': person[6],
                        'PhotoPath': person[7]
                    }
                )
        return results

    def UpdatePerson(self, key, firstName, lastName, accountTypeId, password, gender, titleId, photoPath, deleted ):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE Person SET FirstName = %s, LastName = %s, AccountTypeId = %s, Password = %s, Gender = %s, TitleId = %s, PhotoPath = %s, Deleted = %s WHERE (ObjectId=%s)""",
                (firstName, lastName, accountTypeId, password, gender,titleId, photoPath, deleted, key))
            connection.commit()

    # def UpdatePerson(self, person):
    #     with dbapi2.connect(dsn) as connection:
    #         cursor = connection.cursor()
    #         cursor.execute(
    #             """UPDATE Person SET FirstName = %s, LastName = %s, AccountTypeId = %s, Password = %s, Gender = %s, TitleId = %s, PhotoPath = %s, Deleted = %s WHERE (ObjectId=%s)""",
    #             (person.FirstName, person.LastName, person.AccountTypeId, person.Password, person.Gender,person.TitleId, person.PhotoPath, '0', person.ObjectId))
    #         connection.commit()


    def DeletePerson(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM Person WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()





