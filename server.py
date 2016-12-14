from flask import Flask
from flask import render_template, Blueprint
from flask import request, redirect, url_for
from datetime import datetime
import os
import re
import json
import psycopg2 as dbapi2
from handlers import site
from flask_login import LoginManager
from flask_login import login_required, login_user, current_user
from templates_operations.user import*
from passlib.apps import custom_app_context as pwd_context

from classes.operations.project_operations import project_operations
from classes.operations.person_operations import person_operations
from classes.project import Project
from classes.look_up_tables import *
from templates_operations.user import*

#def create_app():
#    app = Flask(__name__)
#    app.config.from_object('settings')
#    app.register_blueprint(site)
#    return app



#def main():
#    app = create_app()
#    app.run()
lm = LoginManager()

@lm.user_loader
def loadUser(userEMail):
    return getUser(userEMail)

def getUser(userEMail):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query = """SELECT Password FROM Users WHERE eMail = %s"""
        cursor.execute(query, (userEMail,))
        user_value = cursor.fetchone()
        if user_value is None:
            return None
        password = user_value[0]
        user = User(userEMail, password)
    return user

app = Flask(__name__)
app.register_blueprint(site)
app.config['UPLOAD_FOLDER'] = 'static/user_images/'
lm.init_app(app)
lm.login_view = 'login_page'

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/', methods=["GET", "POST"])
def first_page():
    return login_page()


@app.route('/login', methods=["GET", "POST"])
def login_page():
    if request.method == 'GET':
        comment = 'Sign in to start your AcademicFreelance life!'
        return render_template('login.html', comment=comment)
    else:
        if 'login' in request.form:
            email = request.form['email']
            user = getUser(email)
            if user is not None:
                password = request.form['password']
                if pwd_context.verify(password, user.password):
                    login_user(user)
                    next_page = request.args.get('next', url_for('site.home_page'))
                    return redirect(next_page)
                else:
                    comment = 'Incorrect password. Please try again!'
                    return render_template('login.html', comment=comment)
            else:
                comment = 'No email is found. Please try again or register!'
                return render_template('login.html', comment=comment)
        comment = 'Sign in to start your AcademicFreelance life!'
        return render_template('login.html', comment=comment)

@app.route('/init_db')
def init_db():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """CREATE TABLE IF NOT EXISTS CVInformationType (
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Department (
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Information (
                ObjectId SERIAL PRIMARY KEY,
                CVId INTEGER NOT NULL,
                InformationTypeId INTEGER NOT NULL,
                Description VARCHAR(500) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS AccountType(
                ObjectId SERIAL PRIMARY KEY,
                AccountTypeName VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS CV(
                ObjectId SERIAL PRIMARY KEY,
                PersonId INTEGER NOT NULL,
                CreatedDate TIMESTAMP NOT NULL,
                UpdatedDate TIMESTAMP NOT NULL,
                CvName VARCHAR(50),
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS CVInformation(
                ObjectId SERIAL PRIMARY KEY,
                CVId INTEGER NOT NULL,
                Description VARCHAR(500) NOT NULL,
                CVInformationTypeId INTEGER NOT NULL,
                StartDate TIMESTAMP ,
                EndDate TIMESTAMP ,
                DELETED BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS ProjectType(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS ProjectThesisType(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS ProjectStatusType(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Person(
                ObjectId SERIAL PRIMARY KEY,
                FirstName VARCHAR(50) NOT NULL,
                LastName VARCHAR(50) NOT NULL,
			    AccountTypeId INTEGER NOT NULL,
			    eMail VARCHAR(100) UNIQUE NOT NULL,
			    Password VARCHAR(400) NOT NULL,
			    Gender BOOLEAN,
			    TitleId INTEGER NOT NULL,
			    PhotoPath VARCHAR(250),
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Users(
                ObjectId SERIAL PRIMARY KEY,
                eMail VARCHAR(100) UNIQUE NOT NULL,
			    Password VARCHAR(400) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS InformationType(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Project(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Description VARCHAR(1000) NOT NULL,
			    ProjectTypeId INTEGER NOT NULL,
			    ProjectThesisTypeId INTEGER,
			    DepartmentId INTEGER NOT NULL,
			    ProjectStatusTypeId INTEGER NOT NULL,
			    StartDate TIMESTAMP NOT NULL,
			    EndDate TIMESTAMP,
			    MemberLimit INTEGER,
			    TeamId INTEGER,
			    CreatedByPersonId INTEGER NOT NULL,
			    ProjectManagerId INTEGER NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Language(
                ObjectId SERIAL PRIMARY KEY,
                CVId INTEGER NOT NULL,
                Name VARCHAR(50) NOT NULL,
                Level VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS ProjectComment(
                ObjectId SERIAL PRIMARY KEY,
                PersonId INTEGER NOT NULL,
                CommentedProjectId INTEGER NOT NULL,
                Comment VARCHAR(500) NOT NULL,
                CreateDate TIMESTAMP NOT NULL,
                UpdateDate TIMESTAMP NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS PersonComment(
                ObjectId SERIAL PRIMARY KEY,
                PersonId INTEGER NOT NULL,
                CommentedPersonId INTEGER NOT NULL,
                Comment VARCHAR(500) NOT NULL,
                CreateDate TIMESTAMP NOT NULL,
                UpdateDate TIMESTAMP NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Team(
                ObjectId SERIAL PRIMARY KEY,
                ProjectId INTEGER NOT NULL,
                MemberId INTEGER NOT NULL,
                Duty VARCHAR(500) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS WorkLog (
                ObjectId SERIAL PRIMARY KEY,
                ProjectId INTEGER NOT NULL,
                CommitMessage VARCHAR(500) NOT NULL,
                CreatedDate TIMESTAMP NOT NULL,
                CreatorPersonId INTEGER NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Title(
                ObjectId SERIAL PRIMARY KEY,
                Name VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS FollowedPerson(
                ObjectId SERIAL PRIMARY KEY,
                PersonId INT NOT NULL,
                FollowedPersonId INT NOT NULL,
                StartDate TIMESTAMP NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS FollowedProject(
                ObjectId SERIAL PRIMARY KEY,
                PersonId INT NOT NULL,
                FollowedProjectId INT NOT NULL,
                StartDate TIMESTAMP NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)
        query = """CREATE TABLE IF NOT EXISTS Message(
                ObjectId SERIAL PRIMARY KEY,
                SenderId INT NOT NULL,
                RecieverId INT NOT NULL,
                IsRead BOOLEAN NOT NULL,
                MessageContent VARCHAR(400),
                SendDate TIMESTAMP NOT NULL,
                ReadDate TIMESTAMP NOT NULL,
                UpdateDate TIMESTAMP NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)
        query = """CREATE TABLE IF NOT EXISTS Experience(
                ObjectId SERIAL PRIMARY KEY,
                CVId INT NOT NULL,
                CompanyName VARCHAR(100),
                Description VARCHAR(100),
                ExperiencePosition VARCHAR(100),
                StartDate TIMESTAMP NOT NULL,
                EndDate TIMESTAMP NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Education(
                ObjectId SERIAL PRIMARY KEY,
                CVId INT NOT NULL,
                SchoolName VARCHAR(256) NOT NULL,
                Description VARCHAR(256),
                GraduationGrade VARCHAR(100),
                StartDate VARCHAR(20) NOT NULL,
                EndDate VARCHAR(20),
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)

        query = """CREATE TABLE IF NOT EXISTS Skill(
                ObjectId SERIAL PRIMARY KEY,
                CVId INTEGER NOT NULL,
                Name VARCHAR(50) NOT NULL,
                Level VARCHAR(50) NOT NULL,
                Deleted BOOLEAN NOT NULL
        )"""
        cursor.execute(query)


        cursor.execute("""ALTER TABLE Team ADD FOREIGN KEY(MemberId) REFERENCES Person(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE Team ADD FOREIGN KEY(ProjectId) REFERENCES Project(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE PersonComment ADD FOREIGN KEY(CommentedPersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE PersonComment ADD FOREIGN KEY(PersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE Language ADD FOREIGN KEY(CVId) REFERENCES CV(ObjectId) ON DELETE CASCADE """)
        cursor.execute( """ALTER TABLE Message ADD  FOREIGN KEY(SenderId) REFERENCES Person(ObjectId) ON DELETE CASCADE """)
        cursor.execute( """ALTER TABLE Message ADD  FOREIGN KEY(RecieverId) REFERENCES Person(ObjectId) ON DELETE CASCADE """)
        cursor.execute( """ALTER TABLE Experience ADD  FOREIGN KEY(CVId) REFERENCES CV(ObjectId) ON DELETE  CASCADE """)
        cursor.execute("""ALTER TABLE Information ADD  FOREIGN KEY(InformationTypeId) REFERENCES InformationType(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE CV ADD  FOREIGN KEY(PersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE CVInformation ADD  FOREIGN KEY(CVInformationTypeId) REFERENCES CVInformationType(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE CVInformation ADD  FOREIGN KEY(CVId) REFERENCES CV(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Team ADD  FOREIGN KEY(MemberId) REFERENCES Person(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Team ADD  FOREIGN KEY(ProjectId) REFERENCES Project(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Person ADD  FOREIGN KEY(AccountTypeId) REFERENCES AccountType(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Person ADD FOREIGN KEY(TitleId) REFERENCES Title(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Project ADD FOREIGN KEY(ProjectTypeId) REFERENCES ProjectType(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Project ADD FOREIGN KEY (ProjectThesisTypeId) REFERENCES ProjectThesisType(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Project ADD FOREIGN KEY (DepartmentId) REFERENCES Department(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Project ADD FOREIGN KEY (ProjectStatusTypeId) REFERENCES ProjectStatusType(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Project ADD  FOREIGN KEY(TeamId) REFERENCES Team(ObjectId) ON DELETE SET NULL """)
        cursor.execute("""ALTER TABLE Project ADD FOREIGN KEY (CreatedByPersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Project ADD FOREIGN KEY (ProjectManagerId) REFERENCES Person(ObjectId) ON DELETE CASCADE""")
        cursor.execute("""ALTER TABLE Worklog ADD  FOREIGN KEY(CreatorPersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE Worklog ADD  FOREIGN KEY(ProjectId) REFERENCES Project(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE Project ADD  FOREIGN KEY(TeamId) REFERENCES Team(ObjectId) ON DELETE SET NULL """)
        cursor.execute("""ALTER TABLE FollowedPerson ADD  FOREIGN KEY(PersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE FollowedPerson ADD  FOREIGN KEY(FollowedPersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE FollowedProject ADD  FOREIGN KEY(PersonId) REFERENCES Person(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE FollowedProject ADD  FOREIGN KEY(FollowedProjectId) REFERENCES Project(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE Education ADD FOREIGN KEY (CVId) REFERENCES CV(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE Skill ADD FOREIGN KEY(CVId) REFERENCES CV(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE Information ADD FOREIGN KEY(CVId) REFERENCES CV(ObjectId) ON DELETE CASCADE """)
        cursor.execute("""ALTER TABLE Users ADD FOREIGN KEY(eMail) REFERENCES Person(eMail) ON DELETE CASCADE""")


        cursor.execute("""INSERT INTO AccountType (AccountTypeName, Deleted) VALUES ('Student', '0'), ('Academic', '0')""")
        cursor.execute("""INSERT INTO CVInformationType (Name, Deleted) VALUES ('Education', '0'), ('Ability', '0'), ('Experience', '0'), ('Language', '0')""")
        cursor.execute("""INSERT INTO ProjectType (Name, Deleted) VALUES ('Tubitak Projects' , '0'), ('Competition Projects' , '0'), ('International Conference Projects' , '0'),
                      ('National Conference Projects' , '0'), ('Commercial Projects' , '0'), ('StartUp Project' , '0')""")
        cursor.execute("""INSERT INTO ProjectThesisType (Name, Deleted) VALUES ('Bachelor Projects', '0'), ('Master Projects', '0'), ('PhD Projects', '0')""")
        cursor.execute("""INSERT INTO ProjectStatusType (Name, Deleted) VALUES ('standby', '0'), ('onprogress', '0'), ('done', '0')""")
        cursor.execute("""INSERT INTO Title (Name, Deleted) VALUES ('Prof.' , '0'), ('Prof. Dr.' , '0'), ('Doç. Dr.' , '0'), ('Yrd. Doç. Dr.' , '0'), ('Öğr. Gör.' , '0'), ('Araş. Gör.' , '0'),
                      ('Uzman' , '0'), ('Okutman' , '0'), ('Yrd. Doç' , '0'), ('Doç.' , '0'), ('Engineer' , '0'), ('Asistant' , '0'), ('Student' , '0')""")
        cursor.execute("""INSERT INTO Department (Name, Deleted) VALUES ('Computer Engineering', '0'), ('Civil Engineering', '0'), ('Astronautical Engineering', '0'),
                      ('Molecular Biology and Genetics', '0'), ('Geomatics Engineering', '0'), ('Maritime Transportation and Management Engineering', '0'),
                      ('Marine Engineering', '0'), ('Mineral Processing Engineering ', '0'), ('Electrical Engineering', '0'),
                      ('Manufacturing Engineering', '0'), ('Interior Architecture', '0'), ('Mechatronics', '0'), ('Electronics and Communication Engineering', '0'),
                      ('Bioengineering', '0'), ('Humanities and Social Sciences', '0'), ('Control and Automation Engineering', '0'), ('Environmental Engineering', '0'),
                      ('Industrial Engineering', '0'), ('Physics Engineering ', '0'), ('Food Engineering', '0'), ('Geophysics Engineering', '0'), ('Geological Engineering', '0'),
                      ('Chemistry', '0'), ('Chemistry Engineering', '0'), ('Mining Engineering', '0'), ('Mechanical Engineering', '0'), ('Mathematical Engineering ', '0'),
                      ('Metallurgical and Materials Engineering', '0'), ('Meteorological Engineering', '0'), ('Aeronautical Engineering', '0'), ('Aeronautical Engineering', '0'),
                      ('Economics', '0'), ('Textile Engineering', '0'), ('Urban and Regional Planning', '0'), ('Petroleum and Natural Gas Engineering', '0'), ('Landscape Architecture', '0')""")
        cursor.execute("""INSERT INTO InformationType (Name, Deleted) VALUES ('E-Mail', '0'), ('Telephone', '0'), ('Twitter', '0'),
                          ('LinkedIn', '0'), ('Facebook', '0'),('Instagram', '0'),('Blog', '0'),('MySpace', '0'),
                          ('Tumblr', '0'),('Address', '0')""")

        return redirect(url_for('site.register_page'))

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
        app.config['dsn'] = """user='postgres' password='b_e_BTFVmUQvEpr-arXGfL25XHdaVrCX' host='localhost' port=5432 dbname='dxxbzlpn'"""
    app.secret_key = os.urandom(32)

    app.run(host='0.0.0.0', port=port, debug=debug)
    #app.run()


    


