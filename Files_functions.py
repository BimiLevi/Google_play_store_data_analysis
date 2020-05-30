import json
import pandas as pd

# Complexity time - O(|V|+|E|)
def load_graph_data(json_file):
	from Graph import Graph
	try:
		with open(json_file + '.json', 'r') as graph_load:
			graph_obj = Graph.deserialize((json.load(graph_load)))
			return graph_obj
	except:
		return 'Error'

# Complexity time - O(|V|+|E|)
def save_graph_data(file_name, graph):
	try:
		serialize_data = graph.serialize()
		with open('{}.json'.format(file_name), 'w') as graph_save:
			json.dump(serialize_data, graph_save)
	except:
		return 'Error'

# Pandas - read csv
def read_csv_pandas(file_name):
	data = None
	try:
		data = pd.read_csv(str(file_name))
	except:
		raise Exception('An error has  occurred when trying to load the file ')
	finally:
		return data

def save_json(file_name, data):
	try:
		with open('{}.json'.format(file_name), 'w') as f:
			json.dump(data, f)
	except:
		return 'Error'

def load_json(file_name):
	data = None
	try:
		with open(('{}.json'.format(file_name)), 'r') as f:
			data = json.load(f)
			return data
	except:
		return 'Error'
	finally:
		return data


