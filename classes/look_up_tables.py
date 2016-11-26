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

def GetProjectType():
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        query = """SELECT ObjectId, Name, Deleted FROM ProjectType WHERE Deleted = FALSE"""
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def GetProjectThesisType():
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        query = """SELECT ObjectId, Name, Deleted FROM ProjectThesisType WHERE Deleted = FALSE"""
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def GetDepartment():
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        query = """SELECT ObjectId, Name, Deleted FROM Department WHERE Deleted = FALSE"""
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def GetProjectStatusType():
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        query = """SELECT ObjectId, Name, Deleted FROM ProjectStatusType WHERE Deleted = FALSE"""
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def GetLanguage():
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM Languages WHERE Deleted = FALSE"""
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def GetPersonComment():
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM PersonComment WHERE Deleted = FALSE"""
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def GetTeam():
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        query = """SELECT * FROM Team WHERE Deleted = FALSE"""
        cursor.execute(query)
        results = cursor.fetchall()
    return results