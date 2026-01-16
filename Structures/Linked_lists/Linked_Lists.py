from abc import ABCMeta

from Structures.Linked_lists.Node import Node

class LinkedList(Vector): # ABCMeta - метакласс, который проверяет наличие реализации абстрактных методов текущего подкласса

    def __init__(self):
        self.size = 0
        self.head = None
        self.tail = None
    def __len__(self):

    def __contains__(self, item):

    def __setitem__(self, index, value):

    def __getitem__(self, index):

    def __delitem__(self, index):

    # def increase_memory(self):

    def append(self, item):
        new_node = Node(item)

        if self.head is None and self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next_val = new_node # Меняем ссылку бывшего хвоста с Нан на New_node
            self.tail = self.tail.next_val # Сделали хвостом new_node

        self.size += 1


    def insert(self, index, item):

    def pop(self, index=-1):

    def extend(self, new_array):

    def __iter__(self):