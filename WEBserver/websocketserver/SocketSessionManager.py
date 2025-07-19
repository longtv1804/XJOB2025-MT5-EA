from websocketserver import RemoteClient
from common.Log import *

############################################################################################
#   global variable, sotored the session informations
#   only contains VPS client connected via socket
#   including {'username' : RemoteClient}
############################################################################################
g_remoteClients = {}


############################################################################################
#   logic functions
############################################################################################
def isClientValid(clientAccount, token):
    return clientAccount in g_remoteClients and g_remoteClients[clientAccount].CheckToken(token)

def AddClient(clientAccount, socketio, token, sid):
    g_remoteClients[clientAccount] = RemoteClient(clientAccount, socketio, token, sid)

def RemoveClient(clientname):
    g_remoteClients.pop(clientname, None)

def RemoveClientBySid(sid):
    isRemove = False
    for key,client in g_remoteClients:
        if client.CheckSid(sid):
            g_remoteClients.pop(client.m_clientname, None)
            isRemove = True
    if isRemove == False:
        LOGD(f"not found any client with sid={sid}")

def GetClient(clientname):
    if clientname in g_remoteClients:
        return g_remoteClients[clientname]
    return None

def SendMessageToClient(clientname, message):
    client = GetClient(clientname)
    if client:
        client.SendMessage(message)
    else:
        LOGE(f"Client[{clientname}] Not connect")