from flask import current_app
from flask_login import UserMixin
import psycopg2 as dbapi2
import datetime
from classes.model_config import dsn
class User(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.active = True


    def get_id(self):
        return self.email

    @property
    def is_active(self):
        return self.active


def AddUser(user):
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        query = "INSERT INTO Users (Email, Password, Deleted) VALUES (%s, %s, FALSE )"
        cursor.execute(query, (user.email, user.password))
        connection.commit()


def UpdateUser(pswd, email):
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """UPDATE Users SET Password=%s WHERE (Email=%s)""",
            (pswd, email))
        connection.commit()