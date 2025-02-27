import json
import messages as M

class Newline_Delimited_JSON_Wire:

	#This protocol doesn't do encoding because it requires all payloads to be json compatible
	@classmethod
	def encode_object(cls, obj):
		return obj

	@classmethod
	def decode_message(cls, message):

		match json.loads(message):
			case ['B', msg_type, msg_source, msg_payload]:
				return M.Broadcast_Message(msg_type, msg_source, msg_payload)

			case ['P', msg_type, msg_source, msg_dest, msg_payload]:
				return M.Point_to_Point_Message(msg_type, msg_source, msg_dest, msg_payload)

			case unhandled:
				raise Exception(unhandled)


	@classmethod
	def encode_message(cls, message):
		assert isinstance(message.type, str)
		assert isinstance(message.origin, str)
		if isinstance(message, M.Point_to_Point_Message):
			assert isinstance(message.dest, str)

		payload = cls.encode_object(message.payload)

		match message:
			case M.Point_to_Point_Message():
				return json.dumps(['P', message.type, message.origin, message.dest, message.payload]).encode('utf-8')

			case M.Broadcast_Message():
				return json.dumps(['B', message.type, message.origin, message.payload]).encode('utf-8')

			case unhandled:
				raise Exception(unhandled)


	@classmethod
	def to_bytes(cls, *messages):
		result = b''
		for msg in messages:
			result += cls.encode_message(msg) + b'\n'

		return result

	@classmethod
	def from_bytes(cls, buf):
		result = list()
		while buf:
			message, sep, buf = buf.partition(b'\n')

			if sep:
				result.append(cls.decode_message(message))
			else:
				buf = message
				break


		return result, buf

