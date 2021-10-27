import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask import current_app as app
def get_db():
    if 'db' not in g:
        
        import json
        import mysql.connector
        from mysql.connector import errorcode
        f = current_app.open_resource('userconfig.json')
        config = json.load(f)
        # if app.config['TESTING'] is True:
        #     config['database'] = config['database'] + 'TEST'
        #     print("USING TEST DATABASE!\n\n")
        f.close()
        g.db = mysql.connector.connect(**config, auth_plugin='mysql_native_password')

    return g.db
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
  #  app.cli.add_command(init_db)