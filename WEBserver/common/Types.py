from enum import Enum

class UserType(int):
	CREATOR = 100
	ADMIN = 75
	USER = 50
	VPS_CLIENT = 25

def UserType_ToStr(type):
	if type == UserType.CREATOR:
		return "CREATOR"
	elif type == UserType.ADMIN:
		return "ADMIN"
	elif type == UserType.USER:
		return "USER"
	elif type == UserType.VPS_CLIENT:
		return "VPS_CLIENT"
	else:
		return "UNKOWN"