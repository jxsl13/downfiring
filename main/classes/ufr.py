from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import FileSystemStorage
import json


class Ufr:
	"""docstring for Ufr"""
	def __init__(self, uploaded_file: UploadedFile):
		super(Ufr, self).__init__()
		self.ok = True
		self.error_messages = []
		# UFR file info
		self.file = uploaded_file
		self.ufr_filename = self.file.name
		
		# UFR file meta data
		# will be filled with all the necessary data
		# that has been parsed from the ufr file
		self.data_dict = {
			'announce': '',
			'announce-list': [],
			'comment': {},
			'created by': '',
			'creation date': 0,
			'length': 0,
			'name': '',
			'piece length': 0,
			'pieces': 0,
		}

		self.parse_meta_data()
		if len(self.error_messages) > 0:
			self.ok = False

		self.name = self.data_dict['comment']['name']
		self.enc_filename = self.data_dict['name']
		self.description = self.data_dict['comment']['description']
		self.price = self.data_dict['comment']['price']
		self.size = self.data_dict['length']
		self.owner = self.data_dict['comment']['owner']


	def __del__(self):
		self.file.close()


	def parse_meta_data(self):
		
		skip_token = [
			'info',
		]

		last_seen_key = ''

		for chunk in self.file.chunks():

			try:
				
				data = [bytes([byte]) for byte in chunk]
				if data[0] != b'd':
					raise Exception("Invalid file: Header does not start with d")

				# bytes that contain ascii digits are collected in here.	
				token_len: List[bytes] = []	
				# walker variable
				i = 1
				while i < len(data): # len(data)
					elem = data[i]

					if elem.isdigit() :
						# 
						token_len.append(elem)

					elif elem == b':' and len(token_len) != 0:
						# set indices of token
						token_start_idx = i + 1
						token_end_idx = token_start_idx + int(b''.join(token_len))
					
						# create token from slice
						token = data[token_start_idx:token_end_idx]
						# convert token to string
						str_token = b''.join(token).decode(encoding='utf-8')
					

						if str_token in self.data_dict.keys():
							# set last seen key
							last_seen_key = str_token

							#special handling of the 'pieces' key, which also marks the last key
							if last_seen_key == 'pieces':
								i, self.data_dict[last_seen_key] = parse_integer(token_end_idx, data)
								break

						else:
							if str_token not in skip_token:
								# all following token will be handled by the last seen key
								update_data_dictionary(self.data_dict, last_seen_key, str_token)

						# after handling the token, RESET its length stack		
						token_len = []
						# skip token bytes
						i = token_end_idx
						continue	
					else:
						# following a key, there are sometimes integers, that
						# directly contain the value of the key.
						# Thus we parse integers in here
						if elem == b'i' and data[i+1].isdigit():
							# go to the first digit	& get element
							i += 1

							# set i to the index after the integer, 
							# retrieve parsed integer
							i, number = parse_integer(i, data)
							# set the 
							self.data_dict[last_seen_key] = number
							continue
						else:
							pass	
						
					i += 1	
				# directly leave after first iteration/chunk	
				break	

			except Exception as e:
				self.error_messages.append(f"Unecpected file uploaded. {e}")
				return


def update_data_dictionary(data_dict, key, value):
	"""
	@brief      Based on the default data type that is stored at 
				data_dict[key], a different way to add a value will be used
				integer -> set
				list -> append
				dict -> convert json string to dict and set
	
	@param      data_dict  The data dictionary
	@param      key        The key
	@param      value      The value
	
	@return     nothing
	"""
	t = type(data_dict[key])

	if t == list:
		data_dict[key].append(value)
	elif t == str:
		data_dict[key] = value
	elif t == dict:
		data_dict[key] = json.loads(value)
	elif t == int	:
		data_dict[key] = int(value)
	elif t == float:
		data_dict[key] = float(value)
	else:
		print("Could not find corresponding entry")	
						
def parse_integer(start_idx: int, data_array) -> (int, int):
	"""
	@brief      Parse integer from file
	
	@param      start_idx   The start index, must point to the first digit of the integer
	@param      data_array  The data array
	
	@return     returns the index after the token and the parsed integer
				(index_after_token, parsed_integer)
	"""

	i = start_idx
	elem =  data_array[i]
	integer_bytes: List[bytes] = []
	# walk over all of the digits
	while elem.isdigit():
		integer_bytes.append(elem)
		i += 1
		elem = data_array[i]
						
	# cast to integer	
	integer = int(b''.join(integer_bytes))
	return i, integer






