from flask import Flask, render_template, redirect, url_for
from flask import request as FlaskRequest
from flask import session as Flasksession
from flask import redirect as FlaskRedirect
from flask import jsonify as Flaskjsonify
import secrets

from webapp import Authentication
from common import Constants
from common.Log import *

def login():
    error = None
    if FlaskRequest.method == 'POST':
        l_username = FlaskRequest.form['username']
        l_password = FlaskRequest.form['password']
        if Authentication.hasSession(l_username):
            error = f"Account {l_username} đã đăng nhập, hãy logout phiên trước đó."
        elif Authentication.checkLoginInfo(l_username, l_password) == False:
            error = "Tên đăng nhập hoặc mật khẩu không đúng"
        else:
            l_session_id = secrets.token_hex(16)
            Flasksession[Constants.SESSION_KEY_USERNAME] = l_username           # Lưu vào session
            Flasksession[Constants.SESSION_KEY_SESSION_ID] = l_session_id       # Lưu vào session
            Authentication.addSession(l_username, l_session_id)
            return FlaskRedirect(url_for('home'))
    
    if FlaskRequest.method == 'GET' and Constants.SESSION_KEY_USERNAME in Flasksession and Constants.SESSION_KEY_SESSION_ID in Flasksession:
        l_username = Flasksession[Constants.SESSION_KEY_USERNAME]
        l_session_id = Flasksession[Constants.SESSION_KEY_SESSION_ID]
        if Authentication.checkSession(l_username, l_session_id):
            return FlaskRedirect(url_for('home'))

    return render_template('Login.html', error=error)

@Authentication.require_auth
def logout():
    l_username = Flasksession[Constants.SESSION_KEY_USERNAME]
    Authentication.removeSession(l_username)
    Flasksession.pop(Constants.SESSION_KEY_USERNAME, None)
    Flasksession.pop(Constants.SESSION_KEY_SESSION_ID, None)
    return redirect(url_for('login'))
