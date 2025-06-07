from flask import Flask, jsonify, request
import time

app = Flask(__name__)

@app.route('/ws', methods=['GET'])
def websocket_sim():
	account_id = request.args.get("accountID")  # lấy tham số accountID từ URL

	if not account_id:
		return jsonify({"error": "Missing accountID"}), 400

	# Trả về phản hồi kèm theo accountID
	return jsonify({
		"message": f"Hello from account {account_id}",
		"timestamp": time.time()
	})

@app.route('/echo', methods=['POST'])
def echo():
	data = request.json
	return jsonify({"you_sent": data})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
	
