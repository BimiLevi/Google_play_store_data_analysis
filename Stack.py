from Linked_list import Sortable_linked_list, Node

class Sorted_stack:

	def __init__(self):
		self.stack = Sortable_linked_list()

	def __str__(self):
		return self.stack.__str__()

	def push(self, data):
		self.stack.new_head(data)

	def pop(self):
		if self.is_empty():
			raise Exception('Underflow')
		pop_val = self.stack.head.data
		self.stack.size -= 1
		self.stack.head = self.stack.head.next
		return pop_val

	def top(self):
		if self.is_empty():
			raise Exception('The stack is empty!')
		head = self.stack.head.data
		return head

	def is_empty(self):
		if self.stack.head is None:
			return True
		return False

	def get_size(self):
		stack_size = self.stack.get_ll_size()
		return stack_size


