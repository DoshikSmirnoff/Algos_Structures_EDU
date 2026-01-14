from abc import ABCMeta

from Structures.Dinamic_Array import Vector

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

    def insert(self, index, item):

    def pop(self, index=-1):

    def extend(self, new_array):

    def __iter__(self):