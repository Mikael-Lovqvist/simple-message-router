class Endpoint:
	def __init__(self, wire, remote_socket):
		self.wire = wire
		self.socket = remote_socket
		self.socket_peername = remote_socket.getpeername()
		self.socket_fileno = remote_socket.fileno()
		self.buf = b''
		self.unprocessed_messages = list()
		self.registered = False

	def send_message(self, message):
		self.socket.sendall(self.wire.to_bytes(message))

	def close(self):
		print('Close', self.socket)
		self.socket.close()

	def recv_data(self):
		try:
			received = self.socket.recv(1024)
			if not received:
				self.socket.close()
				return

			self.buf += received
			messages, self.buf = self.wire.from_bytes(self.buf)

			for msg in messages:
				self.handle_message(msg)

		except ConnectionResetError:
			print(f"CONNECTION RESET: {self.socket}")
			#Note - do nothing, EPOLLHUP handles it


	def handle_message(self, message):
		self.unprocessed_messages.append(message)


#TBD - should we even differentiate between roles? Or perhaps we should just deal with queues or other methods for synch
class Client_Endpoint(Endpoint):
	pass

class Server_Endpoint(Endpoint):
	pass