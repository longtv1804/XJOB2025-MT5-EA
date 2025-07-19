import socketio

# Tạo client socket
sio = socketio.Client(logger=True, engineio_logger=True)

# Biến lưu sau khi login thành công
username = None
token = None
msg_count = 1

# Khi kết nối thành công
@sio.event
def connect():
	print("✅ Connected")

@sio.event
def disconnect():
	print("⚠️ Disconnected")

def login(u, p):
	global sio
	sio.emit('CLIENT_LOGIN', {'client_name': u, 'password': p})

@sio.on('CLIENT_LOGIN_OK')
def on_login_ok(data):
	global username, token
	username = data.get('username')
	token = data.get('token')
	print(f"Login ok: user={username}, token={token}")
	# Sau khi login, test gửi tin nhắn
	send_message("hello server!")

@sio.on('CLIENT_LOGIN_NG')
def on_login_error(data):
	print("❌ Login error:", data.get('msg'))
	sio.disconnect()
	
# Xử lý phản hồi server từ tin nhắn
def send_message(msg):
	global msg_count
	if username and token:
		print(f'Send Msg:{msg_count} to Server')
		sio.emit('MSG_RCV_CLIENT_TO_SERVER', {
			'client_name': username,
			'client_token': token,
			'msg': msg
		})
		msg_count += 1
	else:
		print("🔐 you havenot logged in yet, can not send the mesage!")

@sio.on('MSG_RCV_SERVER_TO_CLIENT')
def on_server_msg(data):
	print("📩 Server sent:", data)
	if msg_count <= 10:
		send_message('Hello server')
	else:
		sio.disconnect()
	
def main():
	# Kết nối tới server
	print("start connect")
	sio.connect('http://localhost:8000')  # điều chỉnh domain/port nếu cần

	# Gửi thông tin login sau khi kết nối
	print("start login")
	login('client1', '123456')

	# Chờ các event xảy ra
	print('wait...')
	sio.wait()

if __name__ == '__main__':
	main()