
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
            query = "INSERT INTO Person (FirstName, LastName, AccountTypeId, E_Mail, Password, Gender, TitleId, PhotoPath, Deleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE )"
            cursor.execute(query, (person.FirstName, person.LastName, person.AccountTypeId, person.E_Mail, person.Password, person.Gender, person.TitleId, person.PhotoPath))
            connection.commit()
            self.last_key = cursor.lastrowid
        return cursor.lastrowid

    def GetPersonByObjectId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Person.ObjectId, FirstName || ' ' || LastName as FullName, AccountType.AccountTypeName, E_Mail, Password, Gender, Title.Name, PhotoPath
                        FROM Person
                        INNER JOIN AccountType ON (Person.AccountTypeId = AccountType.ObjectId)
                        INNER JOIN Title ON (Person.TitleId = Title.ObjectId)
                        WHERE (Person.ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()
            result = cursor.fetchone()
        return result

    def update_person(self, key, firstName, lastName, accountTypeId, e_Mail, password, gender, titleId, photoPath, deleted ):
        with dbapi2.connect(self.dbfile) as connection:
            cursor =connection.cursor()
            query = "UPDATE Person SET FirstName=?, LastName=?, AccountTypeId=?, E_Mail=?, Password=?, Gender=?, TitleId=?, PhotoPath=?, Deleted=? WHERE (ObjectId=?)"
            cursor.execute(query, (firstName, lastName, accountTypeId, e_Mail, password, gender, titleId, photoPath, deleted, key))
            connection.commit()


    def delete_person(self, key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM Person WHERE (ObjectId=?)"
            cursor.execute(query, (key,))
            connection.commit()



    def get_people(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT FirstName, LastName, AccountTypeId, E_Mail, Password, Gender, TitleId, PhotoPath, Deleted FROM Person ORDER BY ObjectId"
            cursor.execute(query)
            people = [(key, Person(FirstName, LastName, AccountTypeId, E_Mail, Password, Gender, TitleId, PhotoPath, Deleted)) for key, FirstName, LastName, AccountTypeId, E_Mail, Password, Gender, TitleId, PhotoPath, Deleted in cursor]
        return people

