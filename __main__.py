import socket, os, select, threading, pickle, logging
from newline_delimited_json_serializer import Newline_Delimited_JSON_Wire
import messages as M
import routes as R

from endpoint import Client_Endpoint

#CONFIG
#TODO - move to config module (which may be included by state module)
SERVER_BIND = ('0.0.0.0', 7710)

#TODO - move to state module
#Application events
event_fd = os.eventfd(0, flags=os.EFD_NONBLOCK)
epoll = select.epoll()
epoll.register(event_fd, select.EPOLLIN)

client_fd_lut = dict()
route_origin_lut = dict()

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


server_id = 'temporary-server-id'

wire = Newline_Delimited_JSON_Wire


#TODO - move to client module
def register_client(client_socket):
	#TODO: send greeting message with information about the message hub
	client_ep = Client_Endpoint(wire, client_socket)
	logger.info(f"Client connected: {client_ep.socket_peername}")
	client_fd_lut[client_ep.socket_fileno] = client_ep
	epoll.register(client_socket, select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP | select.EPOLLRDHUP)


def unregister_client(client_ep):
	if client_ep.socket_fileno != -1:
		logger.info(f"Client disconnected: {client_ep.socket_peername}")
		client_fd_lut.pop(client_ep.socket_fileno)
		client_ep.socket_fileno = -1

	if (fileno := client_ep.socket.fileno()) != -1:
		epoll.unregister(fileno)



def message_routing_thread():
	while True:
		events = epoll.poll()

		for fileno, event in events:

			if fileno == event_fd:
				os.eventfd_read(event_fd)
				logger.info(f"Unimplemented notification")

			else:
				client_ep = client_fd_lut[fileno]

				if event & select.EPOLLIN:
					client_ep.recv_data()

					while client_ep.unprocessed_messages:
						msg = client_ep.unprocessed_messages.pop(-1)

						if client_ep.registered:
							assert not isinstance(msg, M.Client_Greeting)
						else:
							assert isinstance(msg, M.Client_Greeting)

							if msg.origin in route_origin_lut:
								client_ep.send_message(M.Server_Error(server_id, 'Client name already in use'))
								client_ep.close()
							else:
								route_origin_lut[msg.origin] = R.Local_Client(client_ep, msg.origin, msg.function, msg.description)
								client_ep.registered = True
								client_ep.send_message(M.Server_Greeting(server_id, len(client_fd_lut)))


				if event & select.EPOLLHUP:
					client_ep.close()
					unregister_client(client_ep)

				if event & select.EPOLLRDHUP:
					unregister_client(client_ep)

				if event & select.EPOLLERR:
					client_ep.close()
					unregister_client(client_ep)


def main():

	listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
	listening_socket.bind(SERVER_BIND)
	listening_socket.listen()
	logger.info(f"Server listening on {SERVER_BIND[0]}:{SERVER_BIND[1]}")

	threading.Thread(target=message_routing_thread, daemon=True).start()

	while True:
		client_socket, _ = listening_socket.accept()
		client_socket.setblocking(False)
		register_client(client_socket)
		os.eventfd_write(event_fd, 1)	#TODO - should we do this?


if __name__ == '__main__':
	main()