class Node:
	def __init__(self, data):
		self.data = data
		self.next = None

class Weighted_node(Node):
	def __init__(self, data, weight):
		super().__init__(data)
		self.weight = weight

class Linked_list:
	def __init__(self):
		self.head = None
		self.size = 0

	def __str__(self):
		current_node = self.head
		list_as_string = ''
		while current_node is not None:
			list_as_string += current_node.data.__str__() + '  '
			current_node = current_node.next
		return list_as_string

	# Complexity Time: O(n)
	# the nodes aren't deleted from memory.
	def delete_node(self, del_node):
		# 1 case - the linked list is empty.
		current_node = self.head
		self.size -= 1
		if current_node is None:
			self.size += 1
			raise ValueError('The linked list is empty')
		# 2 case - the deleted node is the head node.
		elif del_node == current_node.data:
			self.head = current_node.next
		# 3 case - the deleted node is at the middle of the list.
		while current_node is not None:
			if current_node.next is None:
				break
			elif current_node.next.data == del_node:
				deleted_node = current_node.next
				current_node.next = current_node.next.next
				deleted_node.next = None
			else:
				current_node = current_node.next
		else:
			return


	# Complexity Tme: O(1)
	def get_ll_size(self):
		return self.size

class Sortable_linked_list(Linked_list):
	def __init__(self):
		super().__init__()

	# Complexity Time: O(n)
	# new head function - sorting the linked list by average each time a new node is added.
	def new_head(self, data):
		new_node = Node(data)
		self.size += 1
		# cases 1 + 2 - the stack list is empty, the new obj average is bigger then the average that is in the top of the stacked list
		if self.head is None or new_node.data.get_average() > self.head.data.get_average():
			new_node.next = self.head
			self.head = new_node
			return
		# sorting the linked list stack
		current_node = self.head
		new_node_average = new_node.data.get_average()
		while current_node.next is not None:
			if new_node_average > current_node.next.data.get_average():
				new_node.next = current_node.next
				current_node.next = new_node
				return
			current_node = current_node.next
		current_node.next = new_node

	# Complexity Time: O(n)
	def print_list(self):
		current_node = self.head
		while current_node is not None:
			print(current_node.data)
			current_node = current_node.next

	# Complexity Time: O(n)
	def linked_list_to_list(self):
		values_list = []
		current_node = self.head
		while current_node is not None:
			values_list.append(current_node.data)
			current_node = current_node.next
		return values_list

class Weighted_linked_list(Linked_list):
	def __init__(self):
		super().__init__()

	def __str__(self):
		current_node = self.head
		list_as_string = ''
		while current_node is not None:
			list_as_string += current_node.data.__str__() + '(' + str(current_node.weight) + ')  '
			current_node = current_node.next
		return list_as_string

	# Complexity Time: O(1)
	def new_head(self, data, weight):
		new_node = Weighted_node(data, weight)
		self.size += 1
		new_node.next = self.head
		self.head = new_node

	# Complexity Time: O(n)
	def print_list(self):
		current_node = self.head
		while current_node is not None:
			print(list(current_node.data, current_node.weight))
			current_node = current_node.next

	# Complexity Time: O(n)
	def linked_list_to_list(self):
		values_list = []
		current_node = self.head
		while current_node is not None:
			if [current_node.data, current_node.weight] not in values_list:
				values_list.append([current_node.data, current_node.weight])
			current_node = current_node.next
		return values_list

	# Complexity Time: O(n)
	# the key in the df is a vertex (representing part of an edge) , and the value is the weight of the edge,
	def linked_list_to_dict(self):
		dict = {}
		current_node = self.head
		while current_node is not None:
			dict[current_node.data] = current_node.weight
			current_node = current_node.next
		return dict


