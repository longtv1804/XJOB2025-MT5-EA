from common import DatabaseManager
from common.Types import UserType
from common.Log import LOGD,LOGE,LOGI

def InitTestDatabase():
	LOGD("InitTestDatabase() init user/pass for testing!")
	DatabaseManager.init_db()
	DatabaseManager.AddUser("admin", "123", UserType.ADMIN)
	DatabaseManager.AddUser("longtv", "123", UserType.CREATOR)
	DatabaseManager.AddUser("client1", "123", UserType.VPS_CLIENT)
	DatabaseManager.AddUser("client2", "123", UserType.VPS_CLIENT)
	LOGD("InitTestDatabase() done!")

def RemoveTestDatabase():
	LOGD("RemoveTestDatabase() remove user/pass for testing")
	DatabaseManager.init_db()
	DatabaseManager.RemoveUser("admin")
	DatabaseManager.AddUser("longtv")
	DatabaseManager.AddUser("client1")
	DatabaseManager.AddUser("client2")
	LOGD("RemoveTestDatabase() Done!")

def CheckUserLogin(userAccount, userPassword):
	userInfoFromDb = DatabaseManager.GetUser(userAccount)
	if userInfoFromDb is not None and userInfoFromDb['password'] == userPassword:
		return userInfoFromDb
	else:
		return None

def DoTerminate():
	LOGD("DoTerminate()")
	pass


