from flask import Flask
from flask import render_template, Blueprint
from flask import  request, redirect, url_for
from handlers import  site
import datetime
import os



def create_app():
    app = Flask(__name__)
#    app.config.from_object('settings')
    app.register_blueprint(site)
    return app



def main():
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
#    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
#    if VCAP_APP_PORT is not None:
#        port, debug = int(VCAP_APP_PORT), False
#    else:
#        port, debug = 5000, True
#    app = create_app()
