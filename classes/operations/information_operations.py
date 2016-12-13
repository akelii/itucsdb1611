import psycopg2 as dbapi2
from classes.model_config import dsn

class information_operations:
    def __init__(self):
        self.last_key = None

    def add_information(self, informationCVId, information_type_id, description):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Information (CVId, InformationTypeId, Description, Deleted) VALUES (%s, %s, %s, False)"
            cursor.execute(query, (informationCVId, information_type_id, description))
            connection.commit()
            self.last_key = cursor.lastrowid

    def delete_information(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM Information WHERE (ObjectId=%s)"""
            cursor.execute(query, (key,))
            connection.commit()

    def update_information(self, key, description):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE Information SET Description = %s WHERE (ObjectId=%s)""",
                (description, key))
            connection.commit()

    def get_all_information_by_CVId(self, key):
        with dbapi2.connect(dsn) as connection:
            cursor = connection.cursor()
            query = """SELECT Information.ObjectId, Information.CVId, InformationType.Name, Information.Description FROM Information JOIN CV ON(Information.CVId = CV.ObjectId) JOIN InformationType ON(Information.InformationTypeId = InformationType.ObjectId) WHERE (CV.ObjectId = %s)"""
            cursor.execute(query, (key,))
            results = cursor.fetchall()
        return results
