from flask import Flask, url_for, render_template, redirect
from flask import redirect as FlaskRedirect
from flask import jsonify as Flaskjsonify
from flask import session as Flasksession

from webapp import Login
from webapp import Authentication
from common import Constants
from webapp.Login import *

g_app = Flask(__name__)
g_app.secret_key = 'secet-key-dont-share'

#==========================================================================
#			login/logout
#==========================================================================
@g_app.route('/login', methods=['GET', 'POST'])
def login():
    return Login.login()

@g_app.route('/logout', methods=['POST'])
@Authentication.require_auth
def logout():
    Login.logout()

#==========================================================================
#			index/home
#==========================================================================
@g_app.route('/', methods=['GET'])
@Authentication.require_auth
def index():
    return FlaskRedirect(url_for('home'))

@g_app.route('/home')
@Authentication.require_auth
def home():
    l_username = Flasksession[Constants.SESSION_KEY_USERNAME]
    l_session_id = Flasksession[Constants.SESSION_KEY_SESSION_ID]
    return render_template('Home.html', username=l_username, token=l_session_id)


#==========================================================================
#			functions related tables
#==========================================================================
@g_app.route('/api/data')
@Authentication.require_auth
def api_data():
    l_username = Flasksession[Constants.SESSION_KEY_USERNAME]
    l_session_id = Flasksession[Constants.SESSION_KEY_SESSION_ID]
    LOGI(f"get data: user:{l_username} session{l_session_id}")
    return Flaskjsonify({
        'status': 'success',
        'user': l_username,
        'session_id': l_session_id,
        'data': 'Đây là dữ liệu được bảo vệ'
    })