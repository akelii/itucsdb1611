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
				ObjectId INTEGER PRIMARY KEY NOT NULL,
				Name VARCHAR(50) NOT NULL,
				Deleted BIT NOT NULL
                )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Department (
				ObjectId INTEGER PRIMARY KEY NOT NULL,
				Name VARCHAR(50) NOT NULL,
				Deleted BIT NOT NULL
                )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Information (
				ObjectId INTEGER PRIMARY KEY NOT NULL,
				FOREIGN KEY(PersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE,
				FOREIGN KEY(InformationTypeId) REFERENCES InformationType(ObjectId) ON DELETE SET NULL,
				Description VARCHAR(500) NOT NULL,
				Deleted BIT NOT NULL
                )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS AccountType{
                ObjectId INTEGER PRIMARY KEY NOT NULL,
                AccountTypeName VARCHAR(50) NOT NULL,
                Deleted BIT NOT NULL,
        }"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS CV{
                ObjectId INTEGER PRIMARY KEY NOT NULL,
                FOREIGN KEY(PersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE,
                CreatedDate DATE NOT NULL,
                UpdatedDate DATE NOT NULL,
                Deleted BIT NOT NULL,

        }"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS CVInformation{
                ObjectId INTEGER PRIMARY KEY NOT NULL,
                FOREIGN KEY(CVId) REFERENCES CV(ObjectId) ON DELETE CASCADE,
                Description VARCHAR(500) NOT NULL,
                FOREIGN KEY (CVInformationTypeId) REFERENCES CVInformationType(ObjectId) ON DELETE CASCADE,
                StartDate DATE NULLABLE ,
                EndDate DATE NULLABLE,
                DELETED BIT NOT NULL,
        }"""
        cursor.execute(query)

    return redirect(url_for('home_page'))




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
