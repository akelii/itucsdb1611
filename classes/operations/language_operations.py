import psycopg2 as dbapi2
from classes.language import Language
import datetime
from classes.model_config import dsn

class language_operations:
    def __init__(self):
        self.last_key=None

    def AddLanguage(self, language):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Language (CVId, Name, Level, Deleted) VALUES (%s, %s, %s, False)"
            cursor.execute(query, (language.CVId, language.Name, language.Level))
            connection.commit()
            self.last_key = cursor.lastrowid

    # Returns one language selected by CVId and Name
    def GetLanguageByName(self, nameKey, idKey):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Language.Name, Language.Level FROM Language INNER JOIN CV ON(Language.CVId = CV.ObjectId)WHERE (Language.Name = %s AND CV.ObjectId = %s) """
            cursor.execute(query, (nameKey,idKey))
            result = cursor.fetchall()
        return result

    # Returns all languages selected by CVId
    def GetAllLanguagesByCVId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Language.ObjectId, Language.CVId, Language.Name, Language.Level FROM Language INNER JOIN CV ON(Language.CVId = CV.ObjectId) WHERE (CV.ObjectId = %s)"""
            cursor.execute(query, (key,))
            result = cursor.fetchall()
        return result

    def UpdateLanguage(self, key, cvId, name, level, deleted ):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE Language SET CVId = %s, Name = %s, Level = %s, Deleted = %s WHERE (ObjectId=%s)""",
                (cvId, name, level, deleted, key))
            connection.commit()


    def DeleteLanguage(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM Language WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()