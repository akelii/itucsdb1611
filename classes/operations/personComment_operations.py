import psycopg2 as dbapi2
from classes.personComment import PersonComment
import datetime
from classes.model_config import dsn

class personComment_operations:
    def __init__(self):
        self.last_key=None

    def AddPersonComment(self, personComment):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO PersonComment (PersonId, CommentedPersonId, Comment, CreateDate, UpdateDate, Deleted) VALUES (%s, %s, %s, ' "+str(datetime.datetime.now())+"', ' "+str(datetime.datetime.now())+"', False)"
            cursor.execute(query, (personComment.personId, personComment.commentedPersonId, personComment.Comment))
            connection.commit()
            self.last_key = cursor.lastrowid

    # Returns all comments made by a person, selected by person name
    def GetPersonCommentsByPersonId(self, personName):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT PersonComment.Comment, p2.Name, PersonComment.UpdateDate
                       FROM PersonComment
                       INNER JOIN Person AS p1 ON(PersonComment.PersonId = p1.ObjectId)
                       INNER JOIN Person AS p2 ON(PersonComment.CommentedPersonId = p2.ObjectId)
                       WHERE (p1.Name = %s)"""
            cursor.execute(query, (personName))
            result = cursor.fetchall()
        return result

    # Returns all comments received by a person, selected by person name
    def GetPersonCommentsByPersonId(self, commentedPersonName):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT p1.Name, PersonComment.Comment, PersonComment.UpdateDate
                       FROM PersonComment
                       INNER JOIN Person AS p1 ON(PersonComment.PersonId = p1.ObjectId)
                       INNER JOIN Person AS p2 ON(PersonComment.CommentedPersonId = p2.ObjectId)
                       WHERE (p2.Name = %s)"""
            cursor.execute(query, (commentedPersonName))
            result = cursor.fetchall()
        return result



    def UpdatePersonComment(self, key, personId, commentedPersonId, comment, deleted ):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE PersonComment SET PersonId = %s, CommentedPersonId = %s, Comment = %s, UpdateDate = ' "+str(datetime.datetime.now())+"', Deleted = %s WHERE (ObjectId=%s)""",
                (personId, commentedPersonId, comment, deleted, key))
            connection.commit()


    def DeleteTeam(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM PersonComment WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()