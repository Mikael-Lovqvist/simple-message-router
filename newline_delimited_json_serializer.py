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
			case ['E', msg_origin, msg_error_message]:
				return M.Server_Error(msg_origin, msg_error_message)

			case ['B', msg_type, msg_origin, msg_payload]:
				return M.Broadcast_Message(msg_type, msg_origin, msg_payload)

			case ['SG', msg_origin, msg_connection_count]:
				return M.Server_Greeting(msg_origin, msg_connection_count)

			case ['CG', msg_origin, msg_function, msg_description]:
				return M.Client_Greeting(msg_origin, msg_function, msg_description)

			case ['P', msg_type, msg_source, msg_dest, msg_payload]:
				return M.Point_to_Point_Message(msg_type, msg_source, msg_dest, msg_payload)

			case unhandled:
				raise Exception(unhandled)


	@classmethod
	def encode_message(cls, message):

		match message:
			case M.Server_Error():
				assert isinstance(message.origin, str)
				assert isinstance(message.error_message, str)
				return json.dumps(['E', message.origin, message.error_message]).encode('utf-8')

			case M.Server_Greeting():
				assert isinstance(message.origin, str)
				assert isinstance(message.connection_count, int)
				return json.dumps(['SG', message.origin, message.connection_count]).encode('utf-8')

			case M.Client_Greeting():
				assert isinstance(message.origin, str)
				assert isinstance(message.function, str)
				assert isinstance(message.description, str)
				return json.dumps(['CG', message.origin, message.function, message.description]).encode('utf-8')

			case M.Point_to_Point_Message():
				assert isinstance(message.type, str)
				assert isinstance(message.origin, str)
				assert isinstance(message.dest, str)
				payload = cls.encode_object(message.payload)
				return json.dumps(['P', message.type, message.origin, message.dest, payload]).encode('utf-8')

			case M.Broadcast_Message():
				assert isinstance(message.type, str)
				assert isinstance(message.origin, str)
				payload = cls.encode_object(message.payload)
				return json.dumps(['B', message.type, message.origin, payload]).encode('utf-8')

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

