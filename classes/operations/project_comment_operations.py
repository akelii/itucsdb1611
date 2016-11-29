

import psycopg2 as dbapi2
import datetime
from classes.model_config import dsn

class project_comment_operations:
    def __init__(self):
        self.last_key = None


    def add_project_comment(self, ProjectComment):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO ProjectComment(PersonId, CommentedProjectId, Comment, Deleted) VALUES (%s, %s, %s, False )",
                (ProjectComment.PersonId, ProjectComment.CommentedProjectId, ProjectComment.Comment))
            connection.commit()
            self.last_key = cursor.lastrowid

    def delete_project_comment(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("""DELETE FROM ProjectComment WHERE (ObjectId=%s)""", (key,))
            connection.commit()

    def update_project_comment(self, key, Comment, Deleted):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE ProjectComment SET Comment = %s, Deleted = %s WHERE (ObjectId=%s)""",
                (Comment, Deleted, key))
            connection.commit()

    def get_project_comments(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT Person.FirstName,Person.LastName, ProjectComment.Comment, ProjectComment.ObjectId
                              FROM ProjectComment
                              JOIN Project ON(Project.ObjectId=ProjectComment.CommentedProjectId)
                              JOIN Person ON(Person.ObjectId=ProjectComment.PersonId)
                              WHERE (ProjectComment.CommentedProjectId=%s)""", (key,))
            project_comments = cursor.fetchall()
            connection.commit()
        return project_comments
