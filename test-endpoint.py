from endpoint import Endpoint
import messages as M
from newline_delimited_json_serializer import Newline_Delimited_JSON_Wire

import socket

s1, s2 = socket.socketpair()


ep1 = Endpoint(Newline_Delimited_JSON_Wire, s1)
ep2 = Endpoint(Newline_Delimited_JSON_Wire, s2)


ep1.send_message(M.Server_Greeting('some-server', 5))
#ep1.socket.shutdown(socket.SHUT_RDWR)

ep2.recv_data()
ep2.recv_data()
