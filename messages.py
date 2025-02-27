from dataclasses import dataclass

@dataclass
class Abstract_Message:
	type: str
	origin: str

@dataclass
class Broadcast_Message(Abstract_Message):
	payload: object = None

@dataclass
class Point_to_Point_Message(Abstract_Message):
	dest: str
	payload: object = None

