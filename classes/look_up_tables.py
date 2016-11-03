import psycopg2 as dbapi2
import datetime
from classes.model_config import dsn


def GetTitleList():
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        query = """SELECT ObjectId, Name, Deleted FROM Title WHERE Deleted = FALSE """
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def GetCVInformationTypeList():
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        query = """SELECT ObjectId, Name, Deleted FROM CVInformationType WHERE Deleted = FALSE """
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def GetAccountTypeList():
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        query = """SELECT ObjectId, AccountTypeName, Deleted FROM AccountType WHERE Deleted = FALSE """
        cursor.execute(query)
        results = cursor.fetchall()
    return results