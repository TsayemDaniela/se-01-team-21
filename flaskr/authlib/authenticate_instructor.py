#!/usr/bin/env python3

import json
from base64 import b64encode
import mysql.connector
from mysql.connector import errorcode
import cgitb
import sys
import bcrypt
import secrets
import datetime
import os
import http.cookies as Cookie
debug = True



table_names = {
    "i_session": "instructor_session",
    "instructor": "instructor"
}
cookie_name = 'SEG21AUTHINSTRUCTOR'
# creates an instructor session given a user id and a mysql.connector cursor.
# connection must be committed after fct. call.
def create_instructor_session(u_id, cursor):
    authentication_response_dict = {
        'session_id': None,
        "status": 405,
        "description": "an error occurred creating a user session",
        "cookie": None,
    }
    token = secrets.token_bytes()
    token = b64encode(token)
    cursor.execute('SELECT s.instructor_id_fk, s.date, s.session_id from instructor_session s WHERE s.instructor_id_fk = %s', (u_id,))
    for (user_id, date, session_id) in cursor.fetchall():
        if date + datetime.timedelta(minutes=30) < datetime.datetime.utcnow():
            cursor.execute("DELETE FROM instructor_session WHERE session_id = %s", (session_id, ))
    #make sure no clashes occur generating a token id, messy but practical solution
    count = 0
    while True:
        try:
            count+=1
            cursor.execute("INSERT INTO instructor_session (session_id, instructor_id_fk, date) VALUES (%s, %s, %s)", 
            ( token, u_id, datetime.datetime.utcnow()))
            #in case we have a token clash, just try to re-calculate a new token
        except mysql.connector.IntegrityError as err:
            token = b64encode(secrets.token_bytes())
            #just tobe safe
            if count > 20:
                return authentication_response_dict
            continue
        except Exception as err:
            return authentication_response_dict
        #we will break if we successfully execute this
        break
    authentication_response_dict['session_id'] = token.decode('utf-8')
    authentication_response_dict['status'] = 200
    authentication_response_dict['description'] = ""
    respCookie = Cookie.SimpleCookie()
    respCookie[cookie_name] = token.decode('utf-8')
    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    respCookie[cookie_name]['expires'] = expiration_date.strftime("%a, %d %b %Y %H:%M:%S UTC")
    respCookie[cookie_name]['path'] = '/'
    authentication_response_dict["cookie"] = respCookie[cookie_name]
    return authentication_response_dict

#authenticates an incoming request to make sure a user session exists
def authenticate(in_cookie, cursor):
    
    req_response = {
        "status": 405,
        "description": "not authenticated",
        "instructor_id": None,
        "cookie": None
    }
    
    try:
        row_count = cursor.execute('SELECT s.instructor_id_fk, s.date, s.session_id FROM instructor_session s WHERE s.session_id = %s', 
        ( in_cookie,))
        if row_count == 0:
            req_response['description'] = "no user session found in database"
            return req_response
        instructor_id,   date, session_id = cursor.fetchone()
        # set the user_id in the response dictionary
        req_response['instructor_id'] = instructor_id

        # case: user session has expired
        if date + datetime.timedelta(minutes=30) < datetime.datetime.utcnow():
            req_response['description'] = "user session expired"
            req_response['status'] = 440
            # delete current user session since it expired
            cursor.execute("DELETE FROM instructor_session WHERE session_id = %s ", 
            (session_id,  ))
            return req_response
        # update our date in cookie / request
        auth_cookie = Cookie.SimpleCookie()
        auth_cookie[cookie_name] = in_cookie
        curdate = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        auth_cookie[cookie_name]['expires'] = curdate.strftime("%a, %d %b %Y %H:%M:%S UTC")
        auth_cookie[cookie_name]['path'] = "/"
        # set our new cookie for the browser
        
        cursor.execute("UPDATE instructor_session SET date =%s WHERE session_id = %s", (curdate, session_id))
        req_response['cookie'] = auth_cookie[cookie_name]
        req_response['status'] = 200
        req_response['description'] = "successfully authenticated!"
        return req_response

    except Exception as err:
        req_response['description'] = err
        return req_response




