
from classes.person import Person
import sqlite3 as dbapi2

class person_operations:
    def __init__(self, dbfile):
        self.last_key=None
        self.dbfile = dbfile



    def get_person(self, key):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT FirstName, LastName FROM Person WHERE (ObjectID=?)"
            cursor.execute(query, (key,))
            connection.commit()


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


    def add_person(self, person):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Person (FirstName, LastName, AccountTypeId, E_Mail, Password, Gender, TitleId, PhotoPath, Deleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(query, (person.FirstName, person.LastName, person.AccountTypeId, person.E_Mail, person.Password, person.Gender, person.TitleId, person.PhotoPath, person.Deleted))
            connection.commit()
            self.last_key = cursor.lastrowid


    def get_people(self):
        with dbapi2.connect(self.dbfile) as connection:
            cursor = connection.cursor()
            query = "SELECT FirstName, LastName, AccountTypeId, E_Mail, Password, Gender, TitleId, PhotoPath, Deleted FROM Person ORDER BY ObjectId"
            cursor.execute(query)
            people = [(key, Person(FirstName, LastName, AccountTypeId, E_Mail, Password, Gender, TitleId, PhotoPath, Deleted)) for key, FirstName, LastName, AccountTypeId, E_Mail, Password, Gender, TitleId, PhotoPath, Deleted in cursor]
        return people

