from typing import Any
from abc import ABC, abstractmethod
class VectorIterator:
    """
    Класс итератор, необходимый для того, чтобы объекты класса Вектор были итерируемыми.
    Это отдельный класс, объект которого будет возвращаться в качестве результата работы метода __iter__.
    Итератором является то, что обладает магическим методом __next__, который отрабатывает каждый раз, когда
    объект итератора передается во встроенную функцию next.
    """
    def __init__(self, array):
        """
        current - счетчик, дающий нам понять на каком объекте перебора мы находимся
        array - запись Vector
        """
        # print(type(array)) -> <class '__main__.Vector'>
        # print(type(array.array)) -> <class 'list'>
        self.array = array # сюда передан Vector
        self.current = 0

    def to_start(self):
        """
        Метод возвращает положение счетчика на старт
        """
        self.current = 0

# СКОРРЕКТИРОВАЛА
    def to_current(self, value): # добавить обработку отриц значений
        """
        Метод меняет значение счетчика на выбранную нами позицию, но в пределах списка наших элементов
        """
        # print(len(self.array))
        # print(len(self.array.array))

        if 0 <= value < len(self.array):
            self.current = value
        elif len(self.array) <= value < 0:
            value += len(self.array)
            self.current = value
        else:
            print("Введено неверное значение!")

    def __iter__(self):
        """
        Метод позволяет объектам возвращать самих себя в качестве итератора, если мы хотим проитерировать сам
        итератор.
        Этот метод возвращает итератор
        """
        return self

    def __next__(self):
        """
        При каждом вызове метода возвращается следующий элемент и счетчик увеличивается на 1, чтобы при
        последующем вызове вернуть следующий объект.
        StopIteration возникает, когда кончились элементы в массиве
        """
        if self.current < len(self.array):
            result = self.array[self.current] # Возможно [], тк в Векторе метод __getitem__
            self.current += 1
            return result
        raise StopIteration

class Vector(ABC):

    def __init__(self, capacity: int = 4, array: list[Any] | None = None):
        """
        capacity -
        """
        if capacity <= 0:
            raise NotImplementedError("Память должна быть больше 0")

        if array is None:
            self.capacity = capacity
            self.size = 0
            self.array = [None] * self.capacity
        else:
            if capacity < len(array) and capacity != 4:
                raise NotImplementedError("Память должна быть больше длины массива")
            elif capacity == 4 and capacity < len(array): # случай, когда capacity по умолчанию, а массив длиннее capacity
                self.size = len(array)
                self.capacity = len(array) * 2
                self.array = array + [None] * self.capacity
            else:
                self.size = len(array)
                self.capacity = len(array) * 2
                self.array = array + [None] * self.capacity

        print(self.size)

    @abstractmethod
    def __len__(self):
        return self.size

    @abstractmethod
    def __contains__(self, item):
        return item in self.array[:self.size]

    @abstractmethod
    def __setitem__(self, index, value): # дописать про отриц индексы в обрутную сторону (лен + 1)
        if self.size == 0 or index > self.size:
            raise IndexError
        else:
            self.array[index] = value

    @abstractmethod
    def __getitem__(self, index): # дописать про отриц индексы в обрутную сторону (лен + 1)
        if self.size == 0 or index > self.size:
            raise IndexError
        else:
            return self.array[index]

    @abstractmethod
    def __delitem__(self, index): # Добавить обработку индексов, дописать про отриц индексы в обрутную сторону (лен + 1)
       if index > len(self.array) or index < -(len(self.array)):
           raise IndexError
       else:
           if index < 0:
               index += len(self.array)
           unchange_part_right = self.array[index + 1:]
           self.array = self.array[:index]
           self.array += unchange_part_right

    def increase_memory(self):
        if self.size == self.capacity or self.size + 1 >= self.capacity: # убрать и проверить в методах
            self.capacity *= 2
            self.array += (self.capacity - self.size) * [None]

    @abstractmethod
    def append(self, item): # Переписать условия проверки - вынести до += , довыделить память по аналогии с созданием массива (доп метод)
        self.increase_memory()
        for elem in range(len(self.array)):
            if self.array[elem] is None:
                self.array[elem] = item
                break # первый None замена на итем
        self.size += 1 # переписать без цикла с использованием self.size

# СКОРРЕКТИРОВАЛА, переписать по аналогии аппенд
    @abstractmethod
    def insert(self, index, item): # Добавить часть про size, соотношение с capacity, циклом сдвинуть часть массива
        unchange_part_left = self.array[:index] # неизменяемая часть массива (которая не сдвигается) слева
        unchange_part_right = self.array[index + 1:] # неизменяемая часть массива справа
        past_elem = self.array[index] # старый, заменяемый элемент, по индексу
        self.array[index] = item # замена элемента по индексу на новый
        new_elem = self.array[index] # новый элемент, на который меняли
        unchange_part_left += [new_elem, past_elem, unchange_part_right]

# СКОРРЕКТИРОВАЛА, переписать как делайтем
    @abstractmethod
    def remove(self, item):
        elem_index = self.array.index(item) # переписать поиск при помощи алгоритмов
        unchange_part_left = self.array[:elem_index]
        unchange_part_right = self.array[elem_index + 1:]
        del self.array[elem_index]

        unchange_part_left += unchange_part_right

    @abstractmethod
    def pop(self, index=-1): # Добавить, если индекс != -1
        if len(self.array) > 0:
            last_item = self.array[index]
            del self.array[index]
            return last_item
        else:
            raise IndexError

# СКОРРЕКТИРОВАЛА, через вайл инкриз мемори вызывать
    @abstractmethod
    def extend(self, new_array):
        self.array += new_array

    @abstractmethod
    def __iter__(self):
        return VectorIterator(self)


v = Vector(array=[0, 2, 4, 5])

iteration_array = v.__iter__()
print(iteration_array.to_current(1))

k = 0
for i in v:
    k += 1
    print(i, k)

print(len(v))