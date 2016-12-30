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



Class Operations
----------------



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



Class Operations
----------------



Templates
---------
