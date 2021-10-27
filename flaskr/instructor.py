from functools import wraps

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response, abort
)
import bcrypt
from werkzeug.security import check_password_hash, generate_password_hash
import json
from flaskr.db import get_db
from .authlib.authenticate_instructor import (create_instructor_session, authenticate)
import mysql.connector.errors
import secrets
from base64 import b64encode
import string

bp = Blueprint('/instructor', __name__, url_prefix='/instructor')
# a function decorator using flask, this decorator is put as :
# @instructor_registered
# def registered()
#


def instructor_registered(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        db = get_db()
        cursor = db.cursor()
        cook = request.cookies.get('SEG21AUTHINSTRUCTOR')
        if not cook:
            abort(405)
        res = authenticate(cook, cursor)
        # print (res)
        cursor.close()
        db.commit()
        if res['status'] != 200:
            abort(405)
        if 'cookie' in res:
            return f(res, *args, **kwargs)
        else:
            abort(405)
    return decorated_function

def instructor_owned(f):
    @wraps(f)
    @instructor_registered
    def decorated_function(auth_resp, *args, **kwargs):
        incomingjson = request.json
        if not incomingjson:
            abort(400, 'empty json in request body')
        if 'game_id' not in incomingjson:
            abort(400, "expected 'game_id' in request body")
        g_id = incomingjson['game_id']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT g.instructor_id from game g WHERE g.game_id = %s', (g_id, ))
        res = cursor.fetchone()
        if not res:
            abort(400, 'game id does not exist!')
        inst_id  = res[0]
        if inst_id != auth_resp['instructor_id']:
            abort(405, 'instructor is not game owner')
        return f(auth_resp, *args, **kwargs)
    return decorated_function




# creates a game and passwords for all players in the session, requires an active instructor session
@bp.route('/create_game', methods=['GET', 'POST'])
@instructor_registered

def create_game(auth_resp):
    
    db = get_db()
    c = auth_resp['cookie']
    cursor = db.cursor()
    in_json = request.json
    instructor_id = auth_resp['instructor_id']
    #for now we create a password for each player, then get their id
    # TODO leave the key as None if we don't want to include a role in our game
    player_ids = {'distributor': None, 'factory': None, 'wholesaler': None, 'retailer': None}
    player_pass = {'distributor': None, 'factory': None, 'wholesaler': None, 'retailer': None}
    for p in player_ids:
        while True:
            try:
                token = secrets.token_bytes()
                token = b64encode(token)
                alphabet = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(alphabet) for i in range(20))
                cursor.execute('INSERT INTO player_session (session_id, password) values (%s, %s)',
                (token, password))
                cursor.execute('SELECT LAST_INSERT_ID()')
                new_p_id = cursor.fetchone()[0]
                player_ids[p] = new_p_id
                player_pass[p] = password
            except mysql.connector.IntegrityError as e:
                continue
            except Exception as e:
                print('FATAL: error occurred creating game')
                print(e)
                abort(500)
            break

    #now, create the game itself
    # TODO implement custom game creation, this is just proof of concept
    cursor.execute('''INSERT INTO game (
        instructor_id,
        factory_id,
        distributor_id,
        wholesaler_id,
        retailer_id
        ) VALUES ( %s, %s, %s, %s, %s)
        ''', (
            instructor_id,
            player_ids['factory'],
            player_ids['distributor'],
            player_ids['wholesaler'],
            player_ids['retailer']
        )
    )
    cursor.execute('SELECT LAST_INSERT_ID()')
    game_id = cursor.fetchone()[0]
    #now we need to update the players so they point to the correct game instances
    for k in player_ids:
        cursor.execute('UPDATE player_session SET game_id = %s WHERE player_id = %s ',
        (game_id, player_ids[k]  ) )
    # our current response documentation
    resp = {
        "passwords": {k: player_pass[k] for k in player_ids},
        "game_id": game_id
    }
    cursor.close()
    db.commit()
    r = make_response(json.dumps(resp))
    r.set_cookie('SEG21AUTHINSTRUCTOR', c.value, expires=c['expires'], path=c['path'])
    return r

@bp.route('/delete_game', methods=['DELETE, POST'])
@instructor_owned
def delete_game(auth_resp):
    try:
        db = get_db()
        cursor = db.cursor()
        c = auth_resp['cookie']
        g_id = request.json['game_id']
        cursor.execute("DELETE FROM game where game_id = %s", (g_id, ) )
        db.commit()
        cursor.close()
        resp = make_response(json.dumps({'success': True}))
        resp.set_cookie('SEG21AUTHINSTRUCTOR', c.value, expires=c['expires'], path=c['path'])
        return resp, 200
    except Exception as e:
        print(e)
        abort(500, 'an error occurred deleting the game')


