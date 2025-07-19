from flask_socketio import SocketIO, emit, disconnect
from flask import request
import secrets

from webapp.WebApp import g_app
from common.Types import *
from common import Constants
from common import UserManager
from common.Log import LOGD,LOGE,LOGI
from websocketserver import SocketSessionManager

KEY_SOCKET_CLIENT_ACC       = "client_acc"
KEY_SOCKET_PASSWORD         = "password"
KEY_SOCKET_TOKEN            = "client_token"
KEY_SOCKET_CLIENT_MSG       = 'msg'
KEY_SOCKET_CLIENT_MSG_ID    = 'msg_id'

g_socketio = SocketIO(g_app, logger=True, engineio_logger=False, cors_allowed_origins="*") # allow connect from client

############################################################################################
#   client request login 
#   Data:
#       {'client_acc':'xxx', 'password':'abc'}
############################################################################################
@g_socketio.on('CLIENT_LOGIN')
def on_login(data):
    error = None
    if KEY_SOCKET_CLIENT_ACC not in data:
        error = "Data err: lack of account"
    if KEY_SOCKET_CLIENT_ACC not in data:
        error = "Data err: lack of password"
    
    if error is None:
        l_clientAcc = data.get(KEY_SOCKET_CLIENT_ACC)
        l_password = data.get(KEY_SOCKET_PASSWORD)
        userInfo = UserManager.CheckUserInfo(l_clientAcc, l_password)
        if userInfo is not None and userInfo['usertype'] == UserType.VPS_CLIENT:
            token = secrets.token_hex(16)
            SocketSessionManager.AddClient(l_clientAcc, g_socketio, token, request.sid)
            emit('CLIENT_LOGIN_OK', {'username':l_clientAcc, 'token':token})
        else:
            error = "Wrong Account or Password!"
    if error is not None:
        emit('CLIENT_LOGIN_NG', {'msg':error})

############################################################################################
#   authen function for user-token
############################################################################################
def authenticated_only(f):
    def wrapper(data):
        if KEY_SOCKET_CLIENT_ACC not in data or KEY_SOCKET_TOKEN not in data:
            return disconnect()
        l_clientname = data.get(KEY_SOCKET_CLIENT_ACC)
        l_token = data.get(KEY_SOCKET_TOKEN)
        if not SocketSessionManager.isClientValid(l_clientname, l_token):
            return disconnect()
        return f(data)
    return wrapper

############################################################################################
#   the socket client is disconnected:
#   data:
#       {'client_acc':'client1', 'client_token':'xxx'}
############################################################################################
@g_socketio.on('CLIENT_DISCONNECTED')
@authenticated_only
def handle_disconnect():
    l_sid = request.sid
    SocketSessionManager.RemoveClientBySid(l_sid)
    LOGD(f"EVENT CLIENT_DISCONNECTED: {l_sid}")

############################################################################################
#   the client is send the message to server
#   data:
#       {'client_acc':'client1', 'client_token':'xxx', 'msg_id'='123', 'msg'='MSGGGGG'}
#    MSGGGGG ussually is json format
############################################################################################
@g_socketio.on('MSG_RCV_CLIENT_TO_SERVER')
@authenticated_only
def handle_msg(data):
    l_clientname = data.get(KEY_SOCKET_CLIENT_ACC)
    l_token = data.get(KEY_SOCKET_TOKEN)
    l_msg = data.get('msg')
    LOGD(f'EVENT MSG_RCV_CLIENT_TO_SERVER client:{l_clientname} token:{l_token} msg:{l_msg}')
    emit('MSG_RCV_SERVER_TO_CLIENT', {'msg': f'hello:({rcv_count}) client'})
    rcv_count += 1