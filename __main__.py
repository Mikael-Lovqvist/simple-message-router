import socket, os, select, threading, pickle, logging

#CONFIG
#TODO - move to config module (which may be included by state module)
SERVER_BIND = ('0.0.0.0', 7710)

#TODO - move to state module
#Application events
event_fd = os.eventfd(0, flags=os.EFD_NONBLOCK)
client_fd_lut = dict()

#TODO - move to logging config module
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s [%(levelname)s] %(message)s",
	handlers=[
		logging.FileHandler("logs/server.log"),
		logging.StreamHandler()
	]
)

logger = logging.getLogger(__name__)





#TODO - move to client module
def register_client(client_socket):
	#TODO: send greeting message with information about the message hub
	logger.info(f"Client connected: {client_socket.getpeername()}")
	client_fd_lut[client_socket.fileno()] = client_socket

def unregister_client(client_socket):
	#TODO: info message for client log writer
	logger.info(f"Client disconnected: {client_socket.getpeername()}")
	client_fd_lut.pop(client_socket.fileno())



def main():

	listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
	listening_socket.bind(SERVER_BIND)
	listening_socket.listen()
	logger.info(f"Server listening on {SERVER_BIND[0]}:{SERVER_BIND[1]}")

	while True:
		client_socket, _ = listening_socket.accept()
		client_socket.setblocking(False)
		register_client(client_socket)
		epoll.register(client_socket, select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP)
		os.eventfd_write(event_fd, 1)


if __name__ == '__main__':
	main()