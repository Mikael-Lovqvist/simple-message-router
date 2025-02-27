import socket
from newline_delimited_json_serializer import Newline_Delimited_JSON_Wire
import messages as M
from endpoint import Server_Endpoint


HOST, PORT = 'localhost', 7710
wire = Newline_Delimited_JSON_Wire




registered = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

	sock.connect((HOST, PORT))
	ep = Server_Endpoint(Newline_Delimited_JSON_Wire, sock)
	ep.send_message(M.Client_Greeting('mah-client', 'test', 'A silly client'))

	ep.recv_data()
	result = ep.unprocessed_messages.pop(-1)

	print('RESULT', result)

	#print(greeting)
	#print('Connected to server', greeting.origin)




	# buf = b''
	# while True:
	# 	received = sock.recv(1024)
	# 	if not received:
	# 		break

	# 	buf += received
	# 	messages, buf = wire.from_bytes(buf)

	# 	for msg in messages:
	# 		if registered is False:
	# 			assert isinstance(msg, M.Server_Greeting)
	# 			print(f'Connected to server {msg.origin!r} which currently handles {msg.connection_count} connections including ours')
	# 			registered = msg.origin
	# 		else:
	# 			assert not isinstance(msg, M.Server_Greeting)

	# 			print('Got message', msg)
