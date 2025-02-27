from dataclasses import dataclass


@dataclass
class Server_Greeting:
	origin: str
	connection_count: int

@dataclass
class Server_Error:
	origin: str
	error_message: str

@dataclass
class Client_Greeting:
	origin: str
	function: str
	description: str

@dataclass
class Broadcast_Message:
	origin: str
	type: str
	payload: object = None

@dataclass
class Point_to_Point_Message:
	origin: str
	type: str
	dest: str
	payload: object = None

