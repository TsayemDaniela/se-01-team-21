import os

from flask import (Flask, g, redirect, render_template, request, session, url_for, make_response)
from flask_socketio import SocketIO, send, emit
clients = []

socketio = SocketIO()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    socketio.init_app(app, cors_allowed_origins="*")

    from . import auth
    from . import instructor
    from . import db
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(instructor.bp)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template('index.html')

    @socketio.on('connect')
    def connected():
        print ("connected!!")
        clients.append(request.sid)
    @socketio.on('message')
    def handle_message(message):
        send(message)

    @socketio.on('json')
    def handle_json(json):
        send(json, json=True)

    @socketio.on('my event')
    def handle_my_custom_event(json):
        emit('my response', json)

    @socketio.on('disconnect')
    def disconnect():
        print ("disconnected!")
        clients.remove(request.namespace)

    @app.route('/player-login')
    def login_player():    
            return render_template('player-login.html')
    @app.route('/instructor-login')
    def login_instructor():    
        return render_template('instructor-login.html')

    @app.route('/test/')
    def broadcast():
        print(clients)
        for c in clients:
            print("c is : ")
            print(c)
            socketio.emit('message', 'testerino', room=c)
        return('hi')
    
    return app

