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
And it returns the result of query to python code to used in code blocks.

	The following **CRUD** operations are implemented in order.

1. **C** reate

- Basic add operation takes *person* object and add its to related database.


.. code-block:: python

    def AddPerson(self, person):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Person (FirstName, LastName, AccountTypeId, Email, Password, Gender, TitleId, PhotoPath, Deleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FALSE )"
            cursor.execute(query, (person.FirstName, person.LastName, person.AccountTypeId, person.Email, person.Password, person.Gender, person.TitleId, person.PhotoPath))
            connection.commit()
            self.last_key = cursor.lastrowid


2. **R** ead

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



3. **U** pdate


- Basic update operation takes all values related to *person* object and update its values.


.. code-block:: python

    def UpdatePerson(self, key, firstName, lastName, accountTypeId, password, gender, titleId, photoPath, deleted ):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE Person SET FirstName = %s, LastName = %s, AccountTypeId = %s, Password = %s, Gender = %s, TitleId = %s, PhotoPath = %s, Deleted = %s WHERE (ObjectId=%s)""",
                (firstName, lastName, accountTypeId, password, gender,titleId, photoPath, deleted, key))
            connection.commit()



4. **D** elete

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

Class operations about **Followed Person** table is under *./classes/operations/followed_person_operations.py* file.

In this file there are **Followed Person** class method which runs SQL scripts with taken parameters, if any.
And it returns the result of query to python code to used in code blocks.

	The following **CRUD** operations are implemented in order.

1. **C** reate

- Basic add operation takes *followed person* object and add its to related database.


.. code-block:: python

    def AddFollowedPerson(self, followed_person):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO FollowedPerson (PersonId, FollowedPersonId, StartDate, Deleted) VALUES (%s, %s,' "+str(datetime.datetime.now())+"', False)"
            cursor.execute(query, (followed_person.PersonId, followed_person.FollowedPersonId))
            connection.commit()
            self.last_key = cursor.lastrowid


2. **R** ead

    Nuumber of select operations related to *followed person* is **five**. It can be found explanations and code blocks in below segment.

- *GetFollowedPersonByObjectId()* selects one of all entities by given *ObjectId* as parameter.


.. code-block:: python

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



- *GetFollowedPersonList()* selects all entities which **Deleted** columns is false from *Followed Person* table.


.. code-block:: python

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


- *GetFollowedPersonListByPersonId()* selects all people which following of given person as parameter.


.. code-block:: python

    def GetFollowedPersonListByPersonId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedPerson.ObjectId, PersonId, p1.FirstName || ' ' || p1.LastName as PersonFullName,
                        FollowedPersonId, p2.FirstName || ' ' || p2.LastName as FollowedPersonFullName,p2.PhotoPath, StartDate
                        FROM FollowedPerson
                        INNER JOIN Person as p1 ON p1.ObjectId = FollowedPerson.PersonId
                        INNER JOIN Person as p2 ON p2.ObjectId = FollowedPerson.FollowedPersonId
                        WHERE FollowedPerson.PersonId = %s AND FollowedPerson.Deleted = '0' ORDER BY StartDate DESC"""
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
                        'FollowedPersonFullName': followed_person[4], #Takip ettigi insanlar
                        'FollowedPersonPhotoPath': followed_person[5],
                        'StartDate': followed_person[6]
                    }
                )
        return results

- *GetFollowedPersonListByFollowedPersonId()* selects all followers which follow given person as parameter.


.. code-block:: python

    def GetFollowedPersonListByFollowedPersonId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedPerson.ObjectId, PersonId, p1.FirstName || ' ' || p1.LastName as PersonFullName, p1.PhotoPath,
                        FollowedPersonId, p2.FirstName || ' ' || p2.LastName as FollowedPersonFullName,StartDate
                        FROM FollowedPerson
                        INNER JOIN Person as p1 ON p1.ObjectId = FollowedPerson.PersonId
                        INNER JOIN Person as p2 ON p2.ObjectId = FollowedPerson.FollowedPersonId
                        WHERE FollowedPerson.FollowedPersonId = %s AND FollowedPerson.Deleted = '0' ORDER BY StartDate DESC"""
            cursor.execute(query, (key,))
            connection.commit()
            data_array = []
            results = cursor.fetchall()
            for followed_person in results:
                data_array.append(
                    {
                        'ObjectId': followed_person[0],
                        'PersonId': followed_person[1],
                        'PersonFullName': followed_person[2], #O kisiyi kimler takip ediyor
                        'PersonPhotoPath': followed_person[3],
                        'FollowedPersonId': followed_person[4],
                        'FollowedPersonFullName': followed_person[5],
                        'StartDate': followed_person[6]
                    }
                )
        return results

- *GetFollowedPersonByPersonIdAndFollowedPersonId()* selects Follower-Following pair result, if any.
It can be used for searching whether 'A' person follows 'B' person, or not.

.. code-block:: python

    def GetFollowedPersonByPersonIdAndFollowedPersonId(self, personid, followedpersonid):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT FollowedPerson.ObjectId
                       FROM FollowedPerson
                       WHERE (FollowedPerson.PersonId=%s and FollowedPerson.FollowedPersonId=%s AND FollowedPerson.Deleted='0')"""
            cursor.execute(query, (personid, followedpersonid))
            result = cursor.fetchone()
        return result


3. **U** pdate


- Basic update operation takes all values related to *FollowedPerson* object and update its values.


.. code-block:: python

    def UpdatePerson(self, key, personId, followedPersonId, startDate, deleted):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE FollowedPerson SET PersonId = %s, FollowedPersonId = %s, StartDate = %s, Deleted = %s WHERE (ObjectId=%s)""",
                (personId, followedPersonId, startDate, deleted, key))
            connection.commit(



4. **D** elete

- There are two delete method for FollowedPerson. One of them deletes tuple from database as normal way.
And other one does not delete row directly. It just set the **Deleted** attribute as true.


.. code-block:: python

    def DeletePersonWithoutStore(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM FollowedPerson WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()

.. code-block:: python

    def DeletePerson(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE FollowedPerson SET Deleted = TRUE WHERE (ObjectId=%s)""",
                (key,))
            connection.commit()



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

Class operations about **Education** table is under *./classes/operations/education_operations.py* file.

In this file there are **Education** class method which runs SQL scripts with taken parameter, if any.
And it returns the result of query to python code to used in code blocks

	The following **CRUD** operations are implemented in order.

1. **C** reate

- Basic add operation takes *education* object and add its to related database.


.. code-block:: python

    def AddEducation(self, education):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Education (CVId, SchoolName, Description, GraduationGrade, StartDate, EndDate, Deleted) VALUES (%s, %s, %s, %s, %s, %s, FALSE )"
            cursor.execute(query, (education.CVId, education.SchoolName, education.Description, education.GraduationGrade, education.StartDate, education.EndDate))
            connection.commit()
            self.last_key = cursor.lastrowid


2. **R** ead

    Nuumber of select operations related to *person* is **two**. It can be found explanations and code blocks in below segment.

- *GetEducationListByCVId()* selects all education row which belongs to given CV as parameter naming *CVId*.


.. code-block:: python

    def GetEducationListByCVId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Education.ObjectId, SchoolName, Description, GraduationGrade, StartDate, EndDate
                        FROM Education
                        INNER JOIN CV ON (Education.CVId = CV.ObjectId)
                        WHERE (Education.CVId=%s) ORDER BY Education.EndDate DESC """
            cursor.execute(query, (key,))
            connection.commit()
            result = cursor.fetchall()
        return result


- *GetEducationListByActiveCVAndByPersonId()* selects all education information which belongs to given *Person* and also *Active CV* of given *Person*.


.. code-block:: python

    def GetEducationListByActiveCVAndByPersonId(self, personId):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Education.ObjectId, SchoolName, Description, GraduationGrade, StartDate, EndDate
                        FROM Education
                        INNER JOIN CV ON (Education.CVId = CV.ObjectId)
                        INNER JOIN Person ON (CV.PersonId = Person.ObjectId)
                        WHERE (Education.CVId=(Select CV.ObjectId FROM CV
                                              INNER JOIN Person ON (CV.PersonId = Person.ObjectId)
                                              WHERE (Person.ObjectId = %s AND CV.IsActive=TRUE))) ORDER BY Education.EndDate DESC"""
            cursor.execute(query, (personId,))
            connection.commit()
            result = cursor.fetchall()
        return result



3. **U** pdate


- Basic update operation takes all values related to *education* object and update its values.


.. code-block:: python

    def UpdateEducation(self, key, schoolname, description, grade, startdate, enddate):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE Education SET SchoolName = %s, Description = %s, GraduationGrade = %s, StartDate = %s, EndDate = %s WHERE (ObjectId=%s)""",
                (schoolname, description, grade, startdate, enddate, key))
            connection.commit()



4. **D** elete

- Delete method takes *ObjectId* and delete it from database.


.. code-block:: python

    def DeleteEducation(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """UPDATE Education SET Deleted = True WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()




Templates
---------
