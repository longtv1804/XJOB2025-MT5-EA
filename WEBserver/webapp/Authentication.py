from flask import request as FlaskRequest
from flask import session as Flasksession
from flask import render_template
from functools import wraps
from common.Types import UserType
from common import Constants


g_users = {
	"admin": ["123456", UserType.ADMIN],
	"longtv": ["asdf123", UserType.CREATOR]
}

#===================================================================
#				session manager
#===================================================================
g_sessions = {}

def addSession(username, session_id):
	g_sessions[username] = session_id

def removeSession(username):
	g_sessions.pop(username, None)

def hasSession(username):
	return username in g_sessions

def isSessionValid(username, session_id):
	return hasSession(username) and g_sessions[username] == session_id

#===================================================================
#				logic functions
#===================================================================
def require_auth(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if Constants.SESSION_KEY_USERNAME not in Flasksession or Constants.SESSION_KEY_SESSION_ID not in Flasksession:
			return render_template('AuthenFailed.html', error="you haven't logged in yet!")
		
		l_username = Flasksession[Constants.SESSION_KEY_USERNAME]
		l_session_id = Flasksession[Constants.SESSION_KEY_SESSION_ID]

		# Kiểm tra có đủ thông tin
		if not l_username or not l_session_id:
			return render_template('AuthenFailed.html', error="your session is not valid!")

		# So khớp với session lưu trong server
		if isSessionValid(l_username, l_session_id) == False:
			return render_template('AuthenFailed.html', error="Authentication failed!")

		return f(*args, **kwargs)
	return decorated_function

def checkSession(username, session_id):
	if not username or not session_id:
		return False
	if isSessionValid(username, session_id) == False:
		return False
	return True

def checkLoginInfo(username, password):
	if hasSession(username):
		return False
	if username in g_users and g_users[username][0] == password:
		return True
	return False
