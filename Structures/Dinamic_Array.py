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
        capacity - объем выделенной памяти, по умолчанию 4, но можно передать свое значение
        array - передается ли массив при создании экземпляра. По умолчанию не передается
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

    # СКОРРЕКТИРОВАЛА
    @abstractmethod
    def __setitem__(self, index, value): # Надо ли писать про добавление по несуществующему индексу типа insert?
        if self.size == 0 or index >= self.size or index < -self.size:
            raise IndexError
        else:
            self.array[index] = value

    # СКОРРЕКТИРОВАЛА
    @abstractmethod
    def __getitem__(self, index):
        if self.size == 0 or index >= self.size or index < -self.size:
            raise IndexError
        else:
            return self.array[index]

    @abstractmethod
    def __delitem__(self, index):
       if index > len(self.array) or index < -self.size:
           raise IndexError
       else:
           if index < 0:
               index += len(self.array)
           unchange_part_right = self.array[index + 1:]
           self.array = self.array[:index]
           self.array += unchange_part_right
# УБРАТЬ ПРОВЕРКУ
    def increase_memory(self):
        if self.size == self.capacity or self.size + 1 >= self.capacity: # убрать и проверить в методах
            self.capacity *= 2
            self.array += (self.capacity - self.size) * [None]

    # СКОРРЕКТИРОВАЛА
    @abstractmethod
    def append(self, item): # Переписать условия проверки - вынести до += , довыделить память по аналогии с созданием массива (доп метод)
        start_len = self.size
        self.increase_memory()
        self.array[start_len + 1] = item

        # for elem in range(len(self.array)):
        #     if self.array[elem] is None:
        #         self.array[elem] = item
        #         break # первый None замена на итем
        # self.size += 1 # переписать без цикла с использованием self.size

# НЕ ПОНИМАЮ как переписать по аналогии ремув
    @abstractmethod
    def insert(self, index, item): # Добавить часть про size, соотношение с capacity, циклом сдвинуть часть массива
        unchange_part_left = self.array[:index] # неизменяемая часть массива (которая не сдвигается) слева
        unchange_part_right = self.array[index + 1:] # неизменяемая часть массива справа
        self.increase_memory()
        past_elem = self.array[index] # старый, заменяемый элемент, по индексу
        self.array[index] = item # замена элемента по индексу на новый
        new_elem = self.array[index] # новый элемент, на который меняли
        unchange_part_left += [new_elem, past_elem, unchange_part_right]

    # СКОРРЕКТИРОВАЛА
    @abstractmethod
    def remove(self, item):
        # elem_index = self.array.index(item) # переписать поиск при помощи алгоритмов
        # unchange_part_left = self.array[:elem_index]
        # unchange_part_right = self.array[elem_index + 1:]
        # del self.array[elem_index]
        #
        # unchange_part_left += unchange_part_right

        for index in range(self.size): # Использовала линейный поиск, тк неясно упорядочен ли массив
            if self.array[index] == item:
                self.array = self.array[:index] # ошибка
                unchange_part_right = self.array[index + 1:]
                self.array += unchange_part_right
                break # дописать элс

    # СКОРРЕКТИРОВАЛА
    @abstractmethod
    def pop(self, index=-1): # Добавить, если индекс != -1
        # if len(self.array) <= 0:
        #     last_item = self.array[index]
        #     del self.array[index]
        #     return last_item
        # else:
        #     raise IndexError

        if index == -1:
            last_item = self.array[index]
            del self.array[index]
            return last_item

        if -self.size <= index < self.size:
            del_item = self.array[index]
            self.array = self.array[:index] # ошибка, поменять местами
            unchange_part_right = self.array[index + 1:]
            self.array += unchange_part_right
            return del_item
        else:
            raise IndexError


# СКОРРЕКТИРОВАЛА, логику в заметках расписала, чтобы не забыть
    @abstractmethod
    def extend(self, new_array):

        start_len = self.size
        necessary_capacity = self.size + len(new_array)

        while self.size < necessary_capacity:
            self.increase_memory()

        for index in range(len(self.array[:start_len + 1]), necessary_capacity + 1): # пересчитать несесари + первый индекс start переписать
            new_array_index = 0
            self.array[index] = new_array[new_array_index]
            new_array_index += 1

    @abstractmethod
    def __iter__(self):
        return VectorIterator(self)


v = Vector(array=[0, 2, 4, 5])

assert isinstance(v, Vector) # True
assert len(v.array) == 4 # True - size
assert v.capacity >= len(v.array) # True
assert isinstance(v.array, list) # True

iteration_array = v.__iter__()
print(iteration_array.to_current(1))