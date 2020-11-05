import json


def write_to_json(data, datafile):
	"""
	Writes the result data to .json file
	:param data: the dictionary to write to file
	"""
	json_object = json.dumps(data, indent = 4)
	with open(datafile, 'w') as outfile:
		outfile.write(json_object)
		outfile.close()


def read_from_json(datafile):
	"""
	Reads the result data from .json file
	:param datafile: the file to be read from
	"""
	with open(datafile, 'r') as openfile:
		json_object = json.load(openfile)
	return json_object
