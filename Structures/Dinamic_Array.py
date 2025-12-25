from typing import Any
class VectorIterator:

    def __init__(self, array):
        print(type(array)) # <class '__main__.Vector'>
        print(type(array.array)) # <class 'list'>
        self.array = array # сюда записан self Vector
        self.current = 0

    def to_start(self):
        self.current = 0

    def to_current(self, value):
        print(len(self.array))
        print(len(self.array.array))
        if value >= len(self.array) or value < 0:
            print("Введено неверное значение!")
        else:
            self.current = value

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < len(self.array):
            result = self.array[self.current] # Возможно [], тк в Векторе метод гетитем
            self.current += 1
            return result
        raise StopIteration

class Vector:

    def __init__(self, capacity: int = 4, array: list[Any] | None = None):
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

    def __len__(self):
        return self.size

    def __contains__(self, item):
        return item in self.array[:self.size]

    def __setitem__(self, index, value): # Добавить обработку индексов, дописать про отриц индексы в обрутную сторону (лен + 1)
        if self.size == 0 or index > self.size:
            raise IndexError
        else:
            self.array[index] = value

    def __getitem__(self, index): # Добавить обработку индексов, дописать про отриц индексы в обрутную сторону (лен + 1)
        if self.size == 0 or index > self.size:
            raise IndexError
        else:
            return self.array[index]

    def __delitem__(self, index): # Добавить обработку индексов, дописать про отриц индексы в обрутную сторону (лен + 1)
        if self.size == 0 or index > self.size:
            raise IndexError
        else:
            del self.array[index] # если посередине где-то, то надо заменить на None?

    def increase_memory(self):
        if self.size == self.capacity or self.size + 1 >= self.capacity: # оставить одно условие
            self.capacity *= 2
            self.array += (self.capacity - self.size) * [None]


    def append(self, item): # Переписать условия проверки - вынести до += , довыделить память по аналогии с созданием массива (доп метод)
        if self.size == self.capacity or self.size + 1 >= self.capacity: # удалить условия
            Vector.increase_memory(self) # к методам можно обращ через self.
        else:
            self.array += [item] # надо None заменить первый на итем
            self.size += 1

    def insert(self, index, item): # Добавить часть про size, соотношение с capacity, циклом сдвинуть часть массива
        if self.size == self.capacity or self.size + 1 >= self.capacity:
            Vector.increase_memory(self)
        else:
            unchange_part = self.array[:index] # неизменяемая часть массива (которая не сдвигается)
            past_elem = self.array[index] # старый, заменяемый элемент, по индексу
            self.array[index] = item # замена элемента по индексу на новый
            new_elem = self.array[index]

            for elem_index in range(len(self.array[index + 1:])): # не понимаю как здесь обозначить именно изменяемый остаток массива
                elem_index += 1

            # return unchange_part + new_elem + # Тут уточнить про сборку массива итогового

    def remove(self, item):
        elem_index = self.array.index(item) # переписать поиск при помощи алгоритмов
        unchange_part = self.array[:elem_index]
        del self.array[elem_index]

        for elem in self.array[elem_index + 1:]: # Не понимаю как сдвинуть влево. Надо создать пустой список и туда добавлять элементы?
            self.array.index(elem) -= 1

    def pop(self, index=-1): # Добавить, если индекс != -1
        if len(self.array) > 0:
            last_item = self.array[index]
            del self.array[index]
            return last_item
        else:
            raise IndexError

    def extend(self, new_array):
        if self.size + len(new_array) >= self.capacity:
            Vector.increase_memory(self)

        self.array += new_array

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