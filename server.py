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



def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn



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
        
    app = Flask(__name__)
    app.register_blueprint(site)
    app.run(host='0.0.0.0', port=port, debug=debug)
