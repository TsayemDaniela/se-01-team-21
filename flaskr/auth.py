import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response, abort
)
import bcrypt
from werkzeug.security import check_password_hash, generate_password_hash
import json
from flaskr.db import get_db
from .authlib.authenticate_instructor import (create_instructor_session, authenticate)
import mysql.connector.errors
import http.cookies as Cookie

bp = Blueprint('auth', __name__, url_prefix='/auth')
@bp.route('/register', methods=['GET', 'POST'])
def register():
    authentication_response_dict = {
    'session_id': None,
    "status": 405,
    "description": "an error occurred creating a user session",
    "cookie": None,
    }
    if request.method == 'POST':
        incomingjson = request.json
        if not incomingjson:
            authentication_response_dict['description'] = "'name' and 'password' expected in json"
            return make_response(json.dumps(authentication_response_dict)), 405
        error = None
        username = incomingjson['name']
        password = incomingjson['password']
        db = get_db()
        cursor = db.cursor()
        
        if not username:
            error = 'name is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            cursor.execute("SELECT u.instructor_id, u.hash FROM instructor u where u.name = %s LIMIT 1"
            , ( username,))
            usr = cursor.fetchone()
            if usr is None:
                error = "invalid username or passaword"
            else:
                (u_id, u_hash) = usr
                u_hash = str.encode(''.join(u_hash))
                usr_pass = str.encode(password)
                if bcrypt.checkpw(usr_pass, u_hash) is True:
                    res = create_instructor_session(u_id, cursor)
                    c = res['cookie']
                    final_res = make_response(json.dumps(res))
                    final_res.set_cookie('SEG21AUTHINSTRUCTOR', c.value, expires=c['expires'], path=c['path'])
                    db.commit()
                    return final_res, 200

                else:
                    error = "invalid username password"

        flash(error)
        authentication_response_dict['description'] = error

    return make_response(json.dumps(authentication_response_dict)), 405

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    authentication_response_dict = {
    'session_id': None,
    "status": 405,
    "description": "an unknown error",
    "cookie": None,
    }
    incomingjson = request.json
    if not incomingjson:
        authentication_response_dict['description'] = "expected body in request"
        return make_response(json.dumps(authentication_response_dict)), 405
    username = incomingjson['name']
    password = incomingjson['password']
    db = get_db()
    cursor = db.cursor()
    error = None

    if not username:
        error = 'name is required.'
    elif not password:
        error = 'Password is required.'
    if error is None:
        try:
            salt = bcrypt.gensalt()
            usr_pass = str.encode(password)
            hashed = bcrypt.hashpw(usr_pass, salt)
        except Exception as e:
            error = 'an error occurred hashing'
    if error is None:   
        try:
            cursor.execute('''INSERT INTO instructor(name, hash) VALUES (%s, %s)''', 
            (username, hashed ) )
            cursor.execute('SELECT LAST_INSERT_ID()')
            new_u_id = cursor.fetchone()[0]
            authentication_response_dict = create_instructor_session(new_u_id, cursor)
            if not authentication_response_dict['cookie']:
                error = "an error occurred creating a user session"
            else:
                c = authentication_response_dict['cookie']
                final_res = make_response(json.dumps(authentication_response_dict))
                final_res.set_cookie('SEG21AUTHINSTRUCTOR', c.value, expires=c['expires'], path=c['path'])
                db.commit()
                return final_res
        except mysql.connector.IntegrityError as err:
            error = 'name already exists'
    # this branch will execute in all cases where signup was not successful
    authentication_response_dict['description'] = error
    return make_response(json.dumps(authentication_response_dict)), 405
#
@bp.route('/player', methods=['GET', 'POST'])
def signup_player():
    authentication_response_dict = {
    'session_id': None,
    'game_id': None,
    'player_id': None,
    "status": 400,
    "description": "password does not exist!",
    }
    incomingjson = request.json
    if not incomingjson:
        abort(400, 'request body expected')
    if 'password' not in incomingjson:
        abort(400, "'password' expected in request body")
    p = incomingjson['password']
    db = get_db()
    cursor = db.cursor()
    print(p)
    cursor.execute("SELECT p.player_id, p.session_id, p.game_id, p.used FROM player_session p WHERE p.password = %s", (p, ) )
    r = cursor.fetchone()
    if not r:
        return json.dumps(authentication_response_dict), 405
    pid, session, game, used = r
    if used:
        authentication_response_dict['description'] = "password is already used! please pick another one"
        authentication_response_dict['status'] = 410
        return json.dumps(authentication_response_dict), 410
    authentication_response_dict['session_id'] = session
    
    #one-time use password
    cursor.execute("UPDATE player_session SET used=1 WHERE player_id = %s", (pid,))
    db.commit()
    cursor.close()
    authentication_response_dict['game_id'] = game
    authentication_response_dict['player_id'] = pid
    authentication_response_dict['description'] = "successfully authenticated"
    authentication_response_dict['status'] = 200
    cookie = session
    res = make_response(json.dumps(authentication_response_dict))
    res.set_cookie('SEG21AUTHPLAYER', cookie)
    return res

