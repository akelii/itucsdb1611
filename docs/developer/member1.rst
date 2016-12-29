Parts Implemented by Ece Naz Sefercioğlu
========================================

****
CV
****


Table
-----

CV table exists in server.py file.

ObjectId attribute holds the primary key of the CV table.

    .. code-block::sql

        CREATE TABLE IF NOT EXISTS CV(
                ObjectId SERIAL PRIMARY KEY,
                PersonId INTEGER NOT NULL,
                CreatedDate TIMESTAMP NOT NULL,
                UpdatedDate TIMESTAMP NOT NULL,
                CvName VARCHAR(50),
                Deleted BOOLEAN NOT NULL,
                IsActive BOOLEAN
        )

    .. code-block::sql

        ALTER TABLE CV ADD  FOREIGN KEY(PersonId)
        REFERENCES Person(ObjectId) ON DELETE CASCADE


PersonId attribute references Person table’s ObjectId attribute.



Class
-----

CV class exists in CV.py file which is in classes folder.

    .. code-block:: python

        class CV:
            def __init__(self, objectId, personId, createdDate, updatedDate, cvname, isActive):
                self.ObjectId = objectId
                self.PersonId = personId
                self.CreatedDate = createdDate
                self.UpdatedDate = updatedDate
                self.CVName = cvname
                self.IsActive=isActive
                self.Deleted = 0



Class Operations
----------------
CV's class operations exists in CV_operations.py which is in **classes/operations** folder.


- The following database operations are implemented for CV:

    -Add Operation

    .. code-block:: python

        def add_cv_with_key(self, cvName,key):
            cvStore=cv_operations()
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                currentCV=cvStore.get_cv(key)
                query = "INSERT INTO CV ( PersonId, CreatedDate, UpdatedDate, CvName, Deleted) VALUES (%s, NOW(), NOW(), %s, 'FALSE')"
                cursor.execute(query, (currentCV[1],cvName,))
                connection.commit()
                self.last_key = cursor.lastrowid

 Adds CV to the current person whose id is taken as an input.

     -Delete Operation

    .. code-block:: python

        def delete_cv(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "DELETE FROM CV WHERE (ObjectId=%s)"
                cursor.execute(query, (str(key),))
                connection.commit()
                cursor.close()

Deletes the CV that has the id equal to key.

    -Update Operations

    .. code-block:: python

        def delete_old_active(self, key,person):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "UPDATE CV SET IsActive='FAlSE' WHERE (IsActive='TRUE' AND ObjectId!=%s AND PersonId=%s)"
                cursor.execute(query, (str(key),person,))
                connection.commit()
                cursor.close()
Sets the old active CV nonactive.

    .. code-block:: python

        def set_cv_active(self,key,personKey):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "UPDATE CV SET IsActive='TRUE' WHERE( ObjectId=%s)"
                cursor.execute(query, (key,))
                connection.commit()
                cv_operations.delete_old_active(self,key,personKey)
Sets the given CV active.

    .. code-block:: python

        def update_cv(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "UPDATE CV SET UpdatedDate=NOW() WHERE( ObjectId=%s)"
                cursor.execute(query, (key,))
                connection.commit()

Updates the UpdatedDate of the CV.


    -Select Operations

    .. code-block:: python

        def get_cv(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "SELECT * FROM CV WHERE (ObjectID=%s)"
                cursor.execute(query, (key,))
                connection.commit()
                result = cursor.fetchone()
            return result

Selects CV by id.

    .. code-block:: python

        def get_cvs(self, personId):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "SELECT ObjectId, PersonId, CreatedDate, UpdatedDate, CvName,IsActive FROM CV  WHERE (PersonId=%s)"
                cursor.execute(query, (personId,))
                cvs = [(key, CV(key, PersonId, CreatedDate, UpdatedDate, CvName,IsActive)) for
                       key, PersonId, CreatedDate, UpdatedDate, CvName, IsActive in cursor]
            return cvs
Selects all the CVs.

    .. code-block:: python

        def get_active_cv(self, key):
            with dbapi2.connect(dsn) as connection:
                    cursor = connection.cursor()
                    query = "SELECT * FROM CV WHERE (IsActive='TRUE' AND PersonId=%s)"
                    cursor.execute(query, (key,))
                    connection.commit()
                    result = cursor.fetchone()
                return result
Selects the active CV of a person.


Templates
---------
**cv.html**, **person_detail.html** and **default.html** are the related templates to Cv.

GET/POST Operations
-------------------
cv.py

    .. code-block:: python

        elif request and 'newCvName' in request.form and request.method =='POST':
            cvName=request.form['newCvName']
            store_CV.add_cv_with_key(cvName,key)
            cvs=store_CV.get_cvs(CurrentPerson[0])
        elif request and 'setCVActive' in request.form and request.method=='POST':
            store_CV.set_cv_active(key,CurrentPerson[0])
            updateCV='TRUE'
        elif request and 'DeleteCv' in request.form and request.method =='POST':
            store_CV.delete_cv(key)
            return redirect(url_for('site.personal_cv_page'))
        if updateCV=="TRUE":
            store_CV.update_cv(key)

**********
Experience
**********


Table
-----

Experience table exists in server.py file.

ObjectId attribute holds the primary key of the Experience table.


    .. code-block::sql

        CREATE TABLE IF NOT EXISTS Experience(
                ObjectId SERIAL PRIMARY KEY,
                CVId INT NOT NULL,
                CompanyName VARCHAR(100),
                Description VARCHAR(100),
                ExperiencePosition VARCHAR(100),
                StartDate VARCHAR(7) NOT NULL,
                EndDate VARCHAR(7) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )

    .. code-block::sql

        ALTER TABLE Experience ADD  FOREIGN KEY(CVId)
        REFERENCES CV(ObjectId) ON DELETE  CASCADE

CVId attribute references CV table’s ObjectId attribute.



Class
-----

Experience class exists in Experience.py file which is in classes folder.

    .. code-block:: python

        class Experience:
            def __init__(self, objectId, cvId, description,companyName,startDate,endDate, experiencePosition):
                self.ObjectId = objectId
                self.CVId = cvId
                self.ExperiencePosition = experiencePosition
                self.CompanyName=companyName
                self.Description = description
                self.StartDate = startDate
                self.EndDate = endDate
                self.Deleted = '0'



Class Operations
----------------
Experience's class operations exists in Experience_operations.py which is in **classes/operations** folder.


- The following database operations are implemented for Experience:

    -Add Operation

    .. code-block:: python

        def add_experience(self, CVId, Description, CompanyName, ExperiencePosition,StartDate,EndDate):
           with dbapi2.connect(dsn) as connection:
               cursor = connection.cursor()
               query = "INSERT INTO Experience (CVId, Description, CompanyName, ExperiencePosition, StartDate, EndDate, DELETED) VALUES (%s, %s, %s, %s, %s, %s, FALSE)"
               cursor.execute(query, ( CVId, Description,CompanyName, ExperiencePosition, StartDate, EndDate, ))
               connection.commit()
               self.last_key = cursor.lastrowid
           return cursor.lastrowid

Adds experience to CV.

    -Delete Operation

    .. code-block:: python

        def delete_experience(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "DELETE FROM Experience WHERE (ObjectId=%s)"
                cursor.execute(query, (key,) )
                connection.commit()
                cursor.close()

Deletes experience from CV.

    -Update Operation

    .. code-block:: python

        def update_experience(self, key, description, startDate, endDate, companyName, experiencePosition ):
            with dbapi2.connect(dsn) as connection:
                cursor =connection.cursor()
                query = "UPDATE Experience SET Description=%s, StartDate=%s, EndDate=%s, CompanyName=%s, ExperiencePosition=%s WHERE (ObjectId=%s)"
                cursor.execute(query, (description, startDate, endDate, companyName, experiencePosition,key))
                connection.commit()

Updates the experience of the cv.

    -Select Operation

    .. code-block:: python

        def get_experience(self, key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "SELECT Description, CompanyName, ExperiencePosition, StartDate, EndDate FROM Experience WHERE (ObjectID=%s)"
                cursor.execute(query, (key))
                connection.commit()

Selects a specific experience.

    .. code-block:: python

        def get_experience_s_with_key(self,key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "SELECT ObjectId,CVId,Description, CompanyName, ExperiencePosition, StartDate, EndDate FROM Experience where (cvid=%s)ORDER BY ObjectID"
                cursor.execute(query,(key,))
                experience_s=[(key, Experience( key, CVId, Description, CompanyName,   StartDate, EndDate,ExperiencePosition ))for key, CVId, Description, CompanyName,  StartDate,EndDate,ExperiencePosition in cursor]
            return experience_s
Returns the experiences of a specific CV.

    .. code-block:: python

        def get_experiences_with_key(self,key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "SELECT * FROM Experience where (cvid=%s)ORDER BY ObjectID"
                cursor.execute(query,(key,))
                experience_s=cursor.fetchall()
            return experience_s
Returns the experiences of a specific CV.

Templates
---------
**cv.html**, **person_detail.html** and **default.html** are the related templates to Experience.

GET/POST Operations
-------------------


cv.py

    .. code-block::python

        elif request and 'NewCompanyName' in request.form and request.method=='POST':
            newCompanyName=request.form['NewCompanyName']
            newDescription=request.form['NewDescription']
            newPosition=request.form['NewPosition']
            startDate=request.form['NewStartDate']
            endDate=request.form['NewEndDate']
            store_experience.add_experience(key,newDescription,newCompanyName,newPosition,startDate,endDate)
            experiences=store_experience.get_experience_s_with_key(key)
            updateCV = "TRUE"
        elif request and 'DeleteExperience' in request.form and request.method=='POST':
            deleteId=request.form['HiddenId']
            store_experience.delete_experience(deleteId)
            experiences=store_experience.get_experience_s_with_key(key)
            updateCV = "TRUE"
        elif request and 'UpdateExperience' in request.form and request.method=='POST':
            updateId = request.form['HiddenId']
            updatedCompanyName = request.form['UpdatedCompanyName']
            updatedDescription = request.form['UpdatedDescription']
            updatedPosition = request.form['UpdatedPosition']
            updatedStartDate = request.form['UpdatedStartDate']
            updatedEndDate = request.form['UpdatedEndDate']
            store_experience.update_experience(updateId,updatedDescription,updatedStartDate,updatedEndDate,
                                               updatedCompanyName,updatedPosition)
            experiences = store_experience.get_experience_s_with_key(key)
            updateCV = "TRUE"


*******
Message
*******


Table
-----

Message table exists in server.py file.

ObjectId attribute holds the primary key of the Message table.


    .. code-block::sql

        CREATE TABLE IF NOT EXISTS Message(
                ObjectId SERIAL PRIMARY KEY,
                SenderId INT NOT NULL,
                ReceiverId INT NOT NULL,
                IsRead BOOLEAN NOT NULL,
                MessageContent VARCHAR(400),
                SendDate TIMESTAMP NOT NULL,
                ReadDate TIMESTAMP,
                DeletedBySender BOOLEAN NOT NULL,
                DeletedByReceiver BOOLEAN NOT NULL
        )

    .. code-block::sql

        ALTER TABLE Message ADD  FOREIGN KEY(SenderId)
        REFERENCES Person(ObjectId) ON DELETE CASCADE

    .. code-block::sql

        ALTER TABLE Message ADD  FOREIGN KEY(ReceiverId)
        REFERENCES Person(ObjectId) ON DELETE CASCADE

SenderId attribute references Person table’s ObjectId attribute.

ReceiverId attribute references Person table’s ObjectId attribute.

Class
-----

Message class exists in project.py file which is in classes folder.

    .. code-block:: python

        class Message:
            def __init__(self,objectId,senderId,ReceiverId,IsRead,MessageContent,SendDate, ReadDate):
                self.ObjectId=objectId
                self.SenderId=senderId
                self.ReceiverId=ReceiverId
                self.IsRead=IsRead
                self.MessageContent=MessageContent
                self.SendDate=SendDate
                self.ReadDate=ReadDate
                self.Deleted=0

Class Operations
----------------
Messages's class operations exists in message_operations.py which is in **classes/operations** folder.



- The following database operations are implemented for Message:

    -Add Operation

    .. code-block:: python

        def send_message(self,senderId,receiverId,messageContent):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "INSERT INTO Message(SenderId,ReceiverId, IsRead, MessageContent, SendDate,ReadDate,DeletedBySender,DeletedByReceiver)VALUES(%s,%s,'FALSE',%s,NOW(),NULL,'FALSE' ,'FALSE')"
                cursor.execute(query,(senderId,receiverId,messageContent))

Adds message to database.

    -Delete Operation

    .. code-block:: python

        def delete_messages(self,key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "DELETE FROM Message WHERE (DeletedBySender='TRUE' and DeletedByReceiver='TRUE')"
                cursor.execute(query, (key,))
                connection.commit()
                cursor.close()

If the message is both deleted from the sender and the receiver, deletes the message from database.

    -Update Operations

    .. code-block:: python

        def set_unread_messages_read(self,sender,receiver):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "UPDATE Message SET IsRead='TRUE', ReadDate=NOW() WHERE(SenderId=%s and ReceiverId=%s )"
                cursor.execute(query, (sender,receiver))
                connection.commit()
                cursor.close()

 Sets message read.

    .. code-block:: python

        def delete_messages_sent(self,key, activeUser):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "UPDATE Message SET DeletedBySender='TRUE' WHERE (ObjectId=%s and SenderId=%s )"
                cursor.execute(query, (str(key),str(activeUser),))
                connection.commit()
                cursor.close()
                message_operations.delete_messages(self, key)

Sets message deleted by the sender.

    .. code-block:: python

        def delete_messages_received(self,key, activeUser):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "UPDATE Message SET DeletedByReceiver='TRUE' WHERE(ObjectId=%s and ReceiverId=%s )"
                cursor.execute(query, (str(key),str(activeUser),))
                connection.commit()
                cursor.close()
                message_operations.delete_messages(self,key)

Sets message deleted by the receiver.


    -Select Operation

    .. code-block:: python

        def get_messages_by_id(self,key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query="SELECT * FROM Message WHERE (ObjectId=%s)"
                cursor.execute(query,(key,))
                connection.commit()
                messages=cursor.fetchall()
            return messages

Gets the message by its id.

    .. code-block:: python

        def get_messages_by_sender_id(self,key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query="SELECT * FROM Message WHERE (ReceiverId=%s)"
                cursor.execute(query,(key,))
                connection.commit()
                messages=cursor.fetchall()
            return messages

Gets the message by its sender's id.

    .. code-block:: python

        def get_messages_by_receiver_id(self,key):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "SELECT * FROM Message WHERE (SenderId=%s)"
                cursor.execute(query,(key,))
                connection.commit()
                messages=cursor.fetchall()
            return messages

Gets the message by its receiver's id.

    .. code-block:: python

        def get_received_messages(self,sender,receiver):
            with dbapi2.connect(dsn) as connection:
                cursor = connection.cursor()
                query = "SELECT * FROM Message WHERE (SenderId=%s AND receiverid=%s)"
                cursor.execute(query,(sender,receiver))
                connection.commit()
                messages=cursor.fetchall()
            return messages


Gets the message received from the given person's id.

Templates
---------
**mailbox.html** is the related template to Message.

GET/POST Operations
-------------------

mailbox.py

    .. code-block:: python

        def mailbox_page_config(request):
            sender = person_operations.GetPerson(current_user, current_user.email)[0]
            key = sender
            messageStore=message_operations()
            Messages = messageStore.get_messages_by_id(key)
            peopleStore=person_operations()
            people=peopleStore.GetPersonList()
            person_with_history=messageStore.get_person_with_messaging_background(sender)
            unread=messageStore.get_total_no_of_unread_messages(sender)

            if request=="GET":
                return render_template('mailbox/mailbox.html', current_user=current_user,sender=sender,
                                       messaged=messaged,person_with_history=person_with_history,key=key,Messages=Messages,people=people)
            else:
                if "sendMessage" in request.form:
                    receiver=request.form['Receiver']
                    sender=person_operations.GetPerson(current_user,current_user.email)[0]
                    message=request.form['Message']
                    messageStore.send_message(sender,5,message)
                return render_template('mailbox/mailbox.html',key=key, person_with_history=person_with_history,
                                       unread=unread,sender=sender,current_user=current_user,Messages=Messages,people=people )

        def messages_page_with_key_config(request, key):
            messageStore = message_operations()
            Messages = messageStore.get_messages()
            peopleStore = person_operations()
            people = peopleStore.GetPersonList()
            receiverPerson=peopleStore.GetPersonByObjectId(key)

            sender = person_operations.GetPerson( current_user,current_user.email)[0]
            senderPerson = peopleStore.GetPersonByObjectId(sender)
            receiver_messages=messageStore.get_messages_by_receiver_id(key)
            sent_messages=messageStore.get_messages_by_sender_id(sender)
            received_messages=messageStore.get_received_messages(sender,key)
            messageStore.set_unread_messages_read(key, sender)
            person_with_history = messageStore.get_person_with_messaging_background(sender)


            if request == "GET":
                Messages = messageStore.get_messages()
                return render_template('mailbox/mailbox.html', sent_messages=sent_messages,receiver_messages=receiver_messages,
                                       senderPerson=senderPerson, receiverPerson=receiverPerson,person_with_history=person_with_history,
                                       sender=sender,key=key,Messages=Messages, people=people)
            else:
                if "sendMessage" in request.form:
                    receiver=request.form['sendMessage']
                    sender=person_operations.GetPerson(current_user,current_user.email)[0]
                    message=request.form['Message']
                    messageStore.send_message(sender,receiver,message)
                    Messages=messageStore.get_messages()
                elif request and "deleteMessage" in request.form:
                    deleteId=request.form['deleteMessage']
                    deleterId=request.form['deleter']

                    if request.form['messageType']=="sent":
                        messageStore.delete_messages_sent(deleteId,deleterId)

                    elif request.form['messageType']=="received":
                        messageStore.delete_messages_received(deleteId, deleterId)

                    Messages=messageStore.get_messages()

                return render_template('mailbox/mailbox.html', sent_messages=sent_messages, receiver_messages=receiver_messages,person_with_history=person_with_history,
                                      senderPerson=senderPerson,receiverPerson=receiverPerson,sender=sender, key=key, Messages=Messages, people=people)

