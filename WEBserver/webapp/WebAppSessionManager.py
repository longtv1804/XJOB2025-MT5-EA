

############################################################################################
#	session manager
############################################################################################
g_WebAppSessions = {}

def AddSession(username, session_id):
	g_WebAppSessions[username] = session_id

def RemoveSession(username):
	g_WebAppSessions.pop(username, None)

def HasSession(username):
	return username in g_WebAppSessions

def IsSessionValid(username, session_id):
	return HasSession(username) and g_WebAppSessions[username] == session_id