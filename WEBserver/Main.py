from websocketserver.WebSocketServer import g_socketio, g_app
from common import UserManager
from common.Log import LOGD,LOGE,LOGI

if __name__ == '__main__':
	LOGD(" =========================== Server start! =========================== ")
	UserManager.InitTestDatabase()
	g_socketio.run(g_app, host='0.0.0.0', port=8000)
	UserManager.RemoveTestDatabase()
	UserManager.DoTerminate()
	LOGD(" =========================== Server ENDED! =========================== ")