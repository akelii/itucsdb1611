Parts Implemented by Elif Ak
============================

******
Person
******

Table
-----

Person create table SQL query in *server.py* file under the *init_db()* function.

	There are 10 column in the table which 8 of them is major columns and other 2's are foreign keys.

    .. code-block:: sql

        CREATE TABLE IF NOT EXISTS Person(
                ObjectId SERIAL PRIMARY KEY,
                FirstName VARCHAR(50) NOT NULL,
                LastName VARCHAR(50) NOT NULL,
			    AccountTypeId INTEGER NOT NULL,
			    eMail VARCHAR(100) UNIQUE NOT NULL,
			    Password VARCHAR(400) NOT NULL,
			    Gender BOOLEAN,
			    TitleId INTEGER NOT NULL,
			    PhotoPath VARCHAR(250),
                Deleted BOOLEAN NOT NULL


Here, there are reference sql queries.


    .. code-block:: sql

        ALTER TABLE Person ADD  FOREIGN KEY(AccountTypeId) REFERENCES AccountType(ObjectId) ON DELETE CASCADE


    .. code-block:: sql

        ALTER TABLE Person ADD FOREIGN KEY(TitleId) REFERENCES Title(ObjectId) ON DELETE CASCADE


Class
-----

Class description about **Person** table is under *./classes/person.py* file.

.. code-block:: python

    class Person:
        def __init__(self, objectId, firstName, lastName, accountTypeId, eMail, password, gender, titleId, photoPath, deleted ):
            self.ObjectId = objectId
            self.FirstName = firstName
            self.LastName = lastName
            self.AccountTypeId = accountTypeId
            self.Email = eMail
            self.Password = password
            self.Gender = gender
            self.TitleId = titleId
            self.PhotoPath = photoPath
            self.Deleted = deleted


Class Operations
----------------

Class operations about **Person** table is under *./classes/operations/person_operations.py* file.

In this file there are **Person** class method which runs SQL scripts with taken parameter, if any.
And it returns the result of query to python code to used in code blocks

	The following *CRUD* operations are implemented in order.

	1. **C**reate

	- Basic add operation takes *person* object and add its to related database.


.. code-block:: python

    def AddPerson(self, person):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Person (FirstName, LastName, AccountTypeId, Email, Password, Gender, TitleId, PhotoPath, Deleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE )"
            cursor.execute(query, (person.FirstName, person.LastName, person.AccountTypeId, person.Email, person.Password, person.Gender, person.TitleId, person.PhotoPath))
            connection.commit()
            self.last_key = cursor.lastrowid


	2. **R**ead

	Nuumber of select operations related to *person* is **five**. It can be found explanations and code blocks in below segment.

	- *GetPersonByObjectId()* selects one of all entities by given *ObjectId* as parameter.


.. code-block:: python

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



	- *GetPerson()* select *Current User* which means loggin user by its unique email from database.

.. code-block:: python

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



	- *GetPersonList()* selects all people in the database.

.. code-block:: python

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



	- *GetLastThreePeople()* selects last three members which register to application.



.. code-block:: python

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



	- *GetPersonListExcludePersonId()* select all people except given *PersonId*. For example, selecting all members except for *Current User*.


.. code-block:: python

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


	3. **U**pdate


	- Basic update operation takes all values related to *person* object and update its values.


.. code-block:: python

    def UpdatePerson(self, key, firstName, lastName, accountTypeId, password, gender, titleId, photoPath, deleted ):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE Person SET FirstName = %s, LastName = %s, AccountTypeId = %s, Password = %s, Gender = %s, TitleId = %s, PhotoPath = %s, Deleted = %s WHERE (ObjectId=%s)""",
                (firstName, lastName, accountTypeId, password, gender,titleId, photoPath, deleted, key))
            connection.commit()



	4. **D**elete

	- Delete method takes *ObjectId* and delete it from database.


.. code-block:: python

    def DeletePerson(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM Person WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()




Templates
---------


***************
Followed Person
***************


Table
-----

Followed Person create table SQL query in *server.py* file under the *init_db()* function.

	There are 5 column in the table which 3 of them is major columns and other 2's are foreign keys.

    .. code-block:: sql

        CREATE TABLE IF NOT EXISTS FollowedPerson(
                ObjectId SERIAL PRIMARY KEY,
                PersonId INT NOT NULL,
                FollowedPersonId INT NOT NULL,
                StartDate TIMESTAMP NOT NULL,
                Deleted BOOLEAN NOT NULL


Here, there are reference sql queries.


    .. code-block:: sql

        ALTER TABLE FollowedPerson ADD  FOREIGN KEY(PersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE


    .. code-block:: sql

        ALTER TABLE FollowedPerson ADD  FOREIGN KEY(FollowedPersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE

Class
-----

Class description about **Followed Person** table is under *./classes/followed_person.py* file.

.. code-block:: python

    class FollowedPerson:
        def __init__(self, objectId, personId, followedPersonId, startDate, deleted):
            self.ObjectId = objectId
            self.PersonId = personId
            self.FollowedPersonId = followedPersonId
            self.StartDate = startDate
            self.Deleted = deleted




Class Operations
----------------



Templates
---------


*********
Education
*********



Table
-----

Education create table SQL query in *server.py* file under the *init_db()* function.

	There are 8 column in the table which 7 of them is major columns and other ones is foreign keys.

    .. code-block:: sql

        CREATE TABLE IF NOT EXISTS Education(
                ObjectId SERIAL PRIMARY KEY,
                CVId INT NOT NULL,
                SchoolName VARCHAR(256) NOT NULL,
                Description VARCHAR(256),
                GraduationGrade VARCHAR(100),
                StartDate INT NOT NULL,
                EndDate INT,
                Deleted BOOLEAN NOT NULL


Here, there are reference sql queries.


    .. code-block:: sql

        ALTER TABLE Education ADD FOREIGN KEY (CVId) REFERENCES CV(ObjectId) ON DELETE CASCADE


Class
-----

Class description about **Education** table is under *./classes/education.py* file.

.. code-block:: python

    class Education:
        def __init__(self, objectId, cvId, schoolName, description, graduationGrade, startDate, endDate, deleted ):
            self.ObjectId = objectId
            self.CVId = cvId
            self.SchoolName = schoolName
            self.Description = description
            self.GraduationGrade = graduationGrade
            self.StartDate = startDate
            self.EndDate = endDate
            self.Deleted = deleted



Class Operations
----------------



Templates
---------
