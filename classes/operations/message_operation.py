import psycopg2 as dbapi2
import datetime
from classes.model_config import dsn
from classes.message import Message

class message_operations:
    def __init__(self):
        self.last_key=None


    def get_messages_by_id(self,key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query="SELECT * FROM Message WHERE (ObjectId=%s)"
            cursor.execute(query,(key,))
            connection.commit()
            messages=cursor.fetchall()
        return messages

    def get_messages(self):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM Message ORDER BY SendDate"
            cursor.execute(query, )
            connection.commit()
            messages = cursor.fetchall()
        return messages

    def get_messages_by_sender_id(self,key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query="SELECT * FROM Message WHERE (ReceiverId=%s)"
            cursor.execute(query,(key,))
            connection.commit()
            messages=cursor.fetchall()
        return messages

    def get_messages_by_receiver_id(self,key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM Message WHERE (SenderId=%s)"
            cursor.execute(query,(key,))
            connection.commit()
            messages=cursor.fetchall()
        return messages

    def get_received_messages(self,sender,receiver):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM Message WHERE (SenderId=%s AND receiverid=%s)"
            cursor.execute(query,(sender,receiver))
            connection.commit()
            messages=cursor.fetchall()
        return messages


    def set_unread_messages_read(self,sender,receiver):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "UPDATE Message SET IsRead='TRUE', ReadDate=NOW() WHERE(SenderId=%s and ReceiverId=%s )"
            cursor.execute(query, (sender,receiver))
            connection.commit()
            cursor.close()

    def get_total_no_of_unread_messages(self,key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "Select count(objectid) from message  WHERE( ReceiverId=%s and IsRead='FALSE' )"
            cursor.execute(query, (key,))
            connection.commit()
            unread_messages=cursor.fethone()
            cursor.close()
        return unread_messages

    def get_person_with_messaging_background(self,sender,receiver):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "SELECT * FROM person WHERE (ObjectId=%s OR ObjectId=%s)"
            cursor.execute(query,(sender,sender,))
            connection.commit()
            people=cursor.fetchall()
        return people

    def delete_messages_sent(self,key, activeUser):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "UPDATE Message SET DeletedBySender='TRUE' WHERE (ObjectId=%s and SenderId=%s )"
            cursor.execute(query, (str(key),str(activeUser),))
            connection.commit()
            cursor.close()
            message_operations.delete_messages(self, key)

    def delete_messages_received(self,key, activeUser):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "UPDATE Message SET DeletedByReceiver='TRUE' WHERE(ObjectId=%s and ReceiverId=%s )"
            cursor.execute(query, (str(key),str(activeUser),))
            connection.commit()
            cursor.close()
            message_operations.delete_messages(self,key)

    def delete_messages(self,key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "DELETE FROM Message WHERE (DeletedBySender='TRUE' and DeletedByReceiver='TRUE')"
            cursor.execute(query, (key,))
            connection.commit()
            cursor.close()

    def send_message(self,senderId,receiverId,messageContent):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Message(SenderId,ReceiverId, IsRead, MessageContent, SendDate,ReadDate,DeletedBySender,DeletedByReceiver)VALUES(%s,%s,'FALSE',%s,NOW(),NULL,'FALSE' ,'FALSE')"
            cursor.execute(query,(senderId,receiverId,messageContent))






















