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




Templates Operations
--------------------

In this segment, there are person related web site pages GET/POST methods written in python.


*Register Page* code behind
^^^^^^^^^^^^^^^^^^^^^^^^^

Users can be register in this page. Following python codes explain create person method. Codes can be found under the *templates_operations/register.py*

1. In **GET** request, title and account type lists is sent to front-end side.


.. code-block:: python

	def register_page_config(request):
		if request.method == 'GET':
			listTitle = GetTitleList()
			listAccount = GetAccountTypeList()
			return render_template('register.html', listTitle=listTitle, listAccount=listAccount, info=' ')

2. In **POST** request, it is taken value field coming from user and it is sent to save class operations.


.. code-block:: python

    else:
        if 'register' in request.form:
            PersonProvider = person_operations()
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            eMail = request.form['eMail']
            p = PersonProvider.GetPerson(eMail)
            error = "'"+eMail+"'" + ' is already in use. Do you forget your password?'
            if p is not None:
                listTitle = GetTitleList()
                listAccount = GetAccountTypeList()
                return render_template('register.html', listTitle=listTitle, listAccount=listAccount, info=error)
            pswd = pwd_context.encrypt(request.form['pswd'])
            accountType = request.form['account']
            title = request.form['title']
            file = request.files['file']
            gender = request.form['r1']
            if gender == 'male':
                gender = False
            elif gender == 'female':
                gender = True
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('static/user_images', filename))
            else:
                if gender == 'male':
                    filename = 'noimage_male.jpg'
                else:
                    filename = 'noimage_female.jpg'
            p = Person(None, first_name, last_name, accountType, eMail, pswd, gender, title, filename, False)
            u = User(eMail, pswd)
            PersonProvider.AddPerson(p)
            AddUser(u)
            return redirect(url_for('site.login_page', info=' '))


Coming infromation after front-end side validation control, there are few things to do. It is necessary to control email, if there is already a user which is same email; another user should not register. Because email must be unique.
And also user password is hashed to save securely. Another important thing is that saving image which uploaded by user. If user is not upload image, default images are assigned related to gender.
User images is saved to servers and it is hold as PhotoPath in database. But there is alowed file controls in this point. User coudn't upload  file format except for 'png', 'jpg', 'jpeg', 'gif'.
Following code shows the content of *allowed_file* function.

.. code-block:: python

	ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

	def allowed_file(filename):
		eturn '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



*Personal Page/Settings Tab*  code behind
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users can be register in this page. Following python codes explain update person methods. Codes can be found under the *templates_operations/personal/default.py*

1. In **POST** request, value field is sent to class method after following code block. In like register page, password and profile page operations are done.
Different thing is that if user could not upload photo or he/she does not enter new password, this value is not updated. Without this control, for example updating the *Name* field cause to set empty password and no-image.


.. code-block:: python

    elif request and 'saveProfileSettings' in request.form and request.method == 'POST':
        FollowedPersonProvider = followed_person_operations()
        listFollowing = FollowedPersonProvider.GetFollowedPersonListByPersonId(Current_Person[0])
        listFollowers = FollowedPersonProvider.GetFollowedPersonListByFollowedPersonId(Current_Person[0])
        personComments = comments.GetPersonCommentsByCommentedPersonId(Current_Person[0])
        listTitle = GetTitleList()
        listAccount = GetAccountTypeList()
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        pswd = request.form['pswd']
        accountType = request.form['account']
        title = request.form['title']
        file = request.files['file']
        gender = request.form['r1']
        if gender == 'male':
            gender = False
        elif gender == 'female':
            gender = True
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename != Current_Person[7]:
                file.save(os.path.join('static/user_images', filename))
            else:
                filename = Current_Person[7]
        elif Current_Person[7] is None:
            if gender:
                filename = 'noimage_female.jpg'
            else:
               filename = 'noimage_male.jpg'
        else:
            filename = Current_Person[7]
        if pswd != "":
            pswd = pwd_context.encrypt(request.form['pswd'])
            UpdateUser(pswd, current_user.email)
        PersonProvider.UpdatePerson(Current_Person[0], first_name, last_name, accountType, ' ', gender, title, filename, False)
        return redirect(url_for('site.personal_default_page', Current_Person=Current_Person,
                            listFollowing=listFollowing, listFollowers=listFollowers,
                            personComments=personComments, listAccount=listAccount, listTitle=listTitle))




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

In this segment, there are followed person operations related in web site pages GET/POST methods written in python.


*People Search* code behind
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Users can search and follow peoples server side python code explanation is below. Codes can be found under the *templates_operations/people/search_person.py*

1. In **GET** and **POST** requests are explained together.


.. code-block:: python

	def people_search_person_page_config(request):
		PersonProvider = person_operations()
		FollowedPersonProvider = followed_person_operations()
		Current_Person = PersonProvider.GetPerson(current_user.email)
		listPerson = PersonProvider.GetPersonListExcludePersonId(Current_Person[0])
		if request and 'follow' in request.form and request.method == 'POST':
			toAdd = FollowedPerson(None,Current_Person[0], request.form['follow'], None, None)
			FollowedPersonProvider.AddFollowedPerson(toAdd)
		elif request and 'unfollow' in request.form and request.method == 'POST':
			toDeletedFollowedPerson = FollowedPersonProvider.GetFollowedPersonByPersonIdAndFollowedPersonId(Current_Person[0], request.form['unfollow'])
			FollowedPersonProvider.DeletePerson(toDeletedFollowedPerson[0])
		count = 0
		while (count < len(listPerson)):
			temp = list(listPerson[count])
			temp.append(
				len(FollowedPersonProvider.GetFollowedPersonListByFollowedPersonId(listPerson[count][0])))  # Followers
			temp.append(len(FollowedPersonProvider.GetFollowedPersonListByPersonId(listPerson[count][0])))  # Following
			if not FollowedPersonProvider.GetFollowedPersonByPersonIdAndFollowedPersonId(Current_Person[0],
                                                                                     listPerson[count][0]):
				temp.append(False)  # Emtpy #O kisiyi takip etmiyor yani buton follow olacak
			else:
				temp.append(True)  # Full #O kisiyi takip ediyor yani buton unfollow olacak
			listPerson[count] = tuple(temp)
			count = count + 1
		return render_template('people/search_person.html', listPerson=listPerson)


*PersonProvider* and *FollowedPersonProvider*  are instnaces to connection related class operaitons. *GetPersonListExcludePersonId(Current_Person[0])* methos selects all people except for *Current User*.
**while** code partition appends number of following and followers count to person list to show following/folloers numbers for each person in search person page. And also there is another thing which shows to decide **Follow** or **Unfollow** button.
For this purpose, *GetFollowedPersonByPersonIdAndFollowedPersonId()* methos is used as true or false depends on the whether follow or not.

For **POST** methods is written for take follow or unfollow comments.


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

In this segment, there are education operations related in web site pages GET/POST methods written in python.


*CV Page* code behind
^^^^^^^^^^^^^^^^^^^^^

Users can search and follow peoples server side python code explanation is below. Codes can be found under the *templates_operations/personal/cv.py*

1. In **POST** requests are explained follwing which include partition related to Education information.

- Create education

After clicking add button, user fills the value field in the opened modal.


	.. code-block:: python

        elif request and 'txtSchoolName' in request.form and request.method == 'POST':
            txtSchoolName = request.form['txtSchoolName']
            txtSchoolDesc = request.form['txtSchoolDesc']
            dpSchoolStart = request.form['dpSchoolStart']
            dpSchoolEnd = request.form['dpSchoolEnd']
            txtGrade = request.form['txtGrade']
            e = Education(None, key, txtSchoolName, txtSchoolDesc, txtGrade, dpSchoolStart, dpSchoolEnd, False)
            store_education.AddEducation(e)
            listEducation = store_education.GetEducationListByCVId(key)
            updateCV = "TRUE"


- Update education

Update operations user interface is like adding. Opened modal page (in this time value field fills with updated information) includes updated properties.
Coming values from user data is **POST** and updates its values. After updating operation, new list sent to front-end side.


	.. code-block:: python

        elif request and 'txtUpdateSchoolName' in request.form and request.method == 'POST':
            txtUpdateSchoolName = request.form['txtUpdateSchoolName']
            txtUpdateSchoolDesc = request.form['txtUpdateSchoolDesc']
            dpUpdateSchoolStart = request.form['dpUpdateSchoolStart']
            dpUpdateSchoolEnd = request.form['dpUpdateSchoolEnd']
            txtUpdateGrade = request.form['txtUpdateGrade']
            id = request.form['hfUpdateEducationId']
            store_education.UpdateEducation(id, txtUpdateSchoolName,txtUpdateSchoolDesc,txtUpdateGrade,dpUpdateSchoolStart,dpUpdateSchoolEnd)
            listEducation = store_education.GetEducationListByCVId(key)
            updateCV = "TRUE"



- Delete education

Because of th Delete operation is a **POST** operations following code partitation is run **deleteEducation** button is triggered. Updated list is sent to front-end side.

	.. code-block:: python

        elif request and 'deleteEducation' in request.form and request.method == 'POST':
            deleteIndex = request.form['deleteEducation']
            store_education.DeleteEducationWithoutStore(deleteIndex)
            listEducation = store_education.GetEducationListByCVId(key)
            updateCV = "TRUE"





