from Files_functions import load_graph_data

data = load_graph_data('weighted_graph')

temp_dict = {
	"kiryat Shmona": [["Hadera", 1], ["Caesarea", 2], ["Tel-Aviv", 3]],
	"Hadera": [["kiryat Shmona", 1], ["Caesarea", 4], ["Tel-Aviv", 5]],
	"Caesarea": [["Hadera", 4], ["kiryat Shmona", 2]],
	"Tel-Aviv": [["kiryat Shmona", 3], ["Hadera", 5]]
             }

print(data)
print('-----------------------------')

# check get vertices
print('get vertices')
print(data.get_vertices())
print('-----------------------------')

# check get edges
print(' get edges ')
print(data.get_edges())
print(len(data.get_edges()))
print('-----------------------------')

# check  BFS
print('BFS')
print(data.BFS('Tel-Aviv', 'kiryat Shmona'), '\n')
# print(data.BFS("Tel-Aviv", "Netanya"), '\n')
print(data.BFS("Tel-Aviv", "Rishon-Lezion"))
print('-----------------------------')


# check get paths head
print('get paths head ')
print(data.get_paths_head(2, 'asc', "Tel-Aviv", "Netanya"), '\n')
print(data.get_paths_head(2, 'desc', "Tel-Aviv", "Netanya"), '\n')
print('-----------------------------')


# check shortest path
print('shortest path')
print(data.shortest_path("Tel-Aviv", "Netanya"), '\n')
print('-----------------------------')


# check add vertex
print('add vertex')
data.add_vertex_from_dict(temp_dict)
print('-----------------------------')


# check delete vertex
print('delete vertex ')
data.delete_vertex("Rishon-Lezion")
print('-----------------------------')


# check graph visualisation
print('graph visualisation')
data.visualise_graph()
print('-----------------------------')


# check serialization
print('serialize')
print(data.serialize())
print('-----------------------------')

print(data)
