from flask import Flask
from flask import render_template, Blueprint
from flask import  request, redirect, url_for
from handlers import  site
import datetime
import os
import re
import json
import psycopg2 as dbapi2

#def create_app():
#    app = Flask(__name__)
#    app.config.from_object('settings')
#    app.register_blueprint(site)
#    return app



#def main():
#    app = create_app()
#    app.run()

app = Flask(__name__)
app.register_blueprint(site)

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/init_db')
def init_db():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS CVInformationType (
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Department (
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Information (
                ObjectId SERIAL PRIMARY KEY,
                PersonId INTEGER NOT NULL,
                InformationTypeId INTEGER NOT NULL,
                Description VARCHAR(500) NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS AccountType(
                ObjectId SERIAL PRIMARY KEY,
                AccountTypeName VARCHAR(50) NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS CV(
                ObjectId SERIAL PRIMARY KEY,
                PersonId INTEGER NOT NULL,
                CreatedDate TIMESTAMP NOT NULL,
                UpdatedDate TIMESTAMP NOT NULL,
                Deleted BIT NOT NULL

        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS CVInformation(
                ObjectId SERIAL PRIMARY KEY,
                CVId INTEGER NOT NULL,
                Description VARCHAR(500) NOT NULL,
                CVInformationTypeId INTEGER NOT NULL,
                StartDate TIMESTAMP ,
                EndDate TIMESTAMP ,
                DELETED BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS ProjectType(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS ProjectThesisType(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS ProjectStatusType(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Person(
                ObjectId SERIAL PRIMARY KEY,
                FirstName VARCHAR(50) NOT NULL,
                LastName VARCHAR(50) NOT NULL,
			    AccountTypeId INTEGER NOT NULL,
			    E_Mail VARCHAR(100) NOT NULL,
			    Password VARCHAR(50) NOT NULL,
			    Gender BIT,
			    TitleId INTEGER NOT NULL,
			    PhotoPath VARCHAR(250),
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS InformationType(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Project(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
			    ProjectTypeId INTEGER NOT NULL,
			    ProjectThesisTypeId INTEGER,
			    DepartmentId INTEGER NOT NULL,
			    ProjectStatusTypeId INTEGER NOT NULL,
			    StartDate TIMESTAMP NOT NULL,
			    EndDate TIMESTAMP,
			    MemberLimit INTEGER,
			    TeamId INTEGER NOT NULL,
			    CreatedByPersonId INTEGER NOT NULL,
			    ProjectManagerId INTEGER NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Team(
                ObjectId SERIAL PRIMARY KEY,
                ProjectId INTEGER NOT NULL,
                MemberId INTEGER NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS WorkLog (
                ObjectId SERIAL PRIMARY KEY,
                ProjectId INTEGER NOT NULL,
                CommitMessage VARCHAR(500) NOT NULL,
                CreatedDate TIMESTAMP NOT NULL,
                CreatorPersonId INTEGER NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Title(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BIT NOT NULL
        )"""
        cursor.execute(query)

        cursor.execute("""ALTER TABLE Information ADD  FOREIGN KEY(PersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Information ADD  FOREIGN KEY(InformationTypeId) REFERENCES InformationType(ObjectId) ON DELETE SET NULL""")
        cursor.execute("""ALTER TABLE CV ADD  FOREIGN KEY(PersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE""")
        cursor.execute( """ALTER TABLE CVInformation ADD  FOREIGN KEY(CVInformationTypeId) REFERENCES CVInformationType(ObjectId) ON DELETE SET NULL""")

    return redirect(url_for('site.home_page'))
    



if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
        
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='dxxbzlpn' password='b_e_BTFVmUQvEpr-arXGfL25XHdaVrCX'
                               host='jumbo.db.elephantsql.com' port=5432 dbname='dxxbzlpn'"""
    app.secret_key = os.urandom(32)
    app.run(host='0.0.0.0', port=port, debug=debug)
