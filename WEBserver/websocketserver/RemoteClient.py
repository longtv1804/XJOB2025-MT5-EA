from common.Log import *

class RemoteClient:
	m_clientaccount = None
	m_token = None
	m_sid = None
	m_socket_reference = None

	#the RemoteClient is paired with this acc
	m_pair = None

	def __init__(self, socket, clientacc, token, sid):
		self.m_socket_reference = socket
		self.m_clientaccount = clientacc
		self.m_token = token
		self.m_sid = sid

	def SetPair(self, remoteClient):
		self.m_pair = remoteClient

	def CheckToken(self, token):
		return token is not None and token == self.m_token
	
	def CheckSid(self, sid):
		return sid is not None and sid == self.m_sid

	#send the message to the client
	def SendMessage(self, message):
		self.m_socket_reference.emit('alert', {'msg': message}, to=self.m_sid)

	def OnMessageReceived(self, msg):
		LOGD(f"OnMessageReceived(): Client[{self.m_clientname}] msg[{msg}]")
		pass