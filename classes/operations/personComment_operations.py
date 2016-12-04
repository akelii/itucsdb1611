import psycopg2 as dbapi2
from classes.personComment import PersonComment
import datetime
from classes.model_config import dsn

class personComment_operations:
    def __init__(self):
        self.last_key=None

    def AddPersonComment(self, personId, commentedPersonId, comment):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO PersonComment (PersonId, CommentedPersonId, Comment, CreateDate, UpdateDate, Deleted) VALUES (%s, %s, %s, ' "+str(datetime.datetime.now())+"', ' "+str(datetime.datetime.now())+"', False)"
            cursor.execute(query, (personId, commentedPersonId, comment))
            connection.commit()
            self.last_key = cursor.lastrowid

    # Returns all comments made by a person, selected by person ID
    def GetPersonCommentsByPersonId(self, personId):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT PersonComment.ObjectId, p2.FirstName ||' '||  p2.LastName as FullName, PersonComment.Comment, PersonComment.UpdateDate, p1.ObjectId, p2.ObjectId
                       FROM PersonComment
                       INNER JOIN Person AS p1 ON(PersonComment.PersonId = p1.ObjectId)
                       INNER JOIN Person AS p2 ON(PersonComment.CommentedPersonId = p2.ObjectId)
                       WHERE (p1.ObjectId = %s)"""
            cursor.execute(query, (personId,))
            result = cursor.fetchall()
        return result

    # Returns all comments received by a person, selected by person ID
    def GetPersonCommentsByCommentedPersonId(self, commentedPersonId):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT PersonComment.ObjectId ,p1.FirstName ||' '||  p1.LastName as FullName, PersonComment.Comment, PersonComment.UpdateDate, p1.ObjectId, p2.ObjectId, p1.PhotoPath
                       FROM PersonComment
                       INNER JOIN Person AS p1 ON(PersonComment.PersonId = p1.ObjectId)
                       INNER JOIN Person AS p2 ON(PersonComment.CommentedPersonId = p2.ObjectId)
                       WHERE (p2.ObjectId = %s) ORDER BY PersonComment.CreateDate DESC"""
            cursor.execute(query, (commentedPersonId,))
            result = cursor.fetchall()
        return result

    # Returns object ids of persons that one of them comments and one of them is commented
    def GetRelatedPersonsIdByCommentId(self, commentId):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT p1.ObjectId, p2.ObjectId
                       FROM PersonComment
                       INNER JOIN Person AS p1 ON(PersonComment.PersonId = p1.ObjectId)
                       INNER JOIN Person AS p2 ON(PersonComment.CommentedPersonId = p2.ObjectId)
                       WHERE (PersonComment.ObjectId = %s)"""
            cursor.execute(query, (commentId,))
            result = cursor.fetchall()
        return result

    def UpdatePersonComment(self, key, comment ):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE PersonComment SET  Comment = %s, UpdateDate = NOW(), Deleted = False WHERE (ObjectId=%s)""",
                (comment, key))
            connection.commit()


    def DeleteTeam(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM PersonComment WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()