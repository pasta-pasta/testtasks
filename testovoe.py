from collections import deque
import time
import random

# Задание 1
'''На языке Python написать алгоритм (функцию) определения четности целого числа, который будет аналогичен нижеприведенному по функциональности, 
но отличен по своей сути. Объяснить плюсы и минусы обеих реализаций. 

Пример: 

def isEven(value):
    return value % 2 == 0'''

def isEven1(value):
    return value & 1 == 0 # побитовое И, если последний бит 0, то число четное

'''Плюсы и минусы реализаций:
1. Плюсы и минусы изначальной реализации:
    + более читаемая, т.к. использует стандартные операции -- наиболее понятна для новичков
    - медленнее в работе, т.к. использует операцию деления
2. Плюсы и минусы новой реализации:
    + быстрее в работе, т.к. не использует операцию деления и может быть портирована на другие языки (например, C++)
    - менее читаемая, т.к. требует знания побитовых операций
'''

# Задание 2
'''На языке Python написать минимум по 2 класса реализовывающих циклический буфер FIFO. Объяснить плюсы и минусы каждой реализации.

Оценивается:

Полнота и качество реализации
Оформление кода
Наличие сравнения и пояснения по быстродействию'''

class FIFO1:
    def __init__(self, cap):
        self.capacity = cap # Размер буфера
        self.queue = [None]*cap
        self.head = 0
        self.tail = 0
        self.size = 0

    def is_full(self): # Проверка на заполненность  
        return self.size == self.capacity
    
    def is_empty(self): # Проверка на пустоту
        return self.size == 0
    
    def enqueue(self, item): # Добавление элемента
        if self.is_full():
            raise Exception("Queue is full")
        self.queue[self.tail] = item
        self.tail = (self.tail + 1) % self.capacity
        self.size += 1

    def dequeue(self): # Удаление элемента
        if self.is_empty():
            raise Exception("Queue is empty")
        item = self.queue[self.head]
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        return item
    
    def peek(self): # Просмотр элемента
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.queue[self.head]
    
    def __str__(self): 
        return str(self.queue)
    
'''Это базовая реализация, использующя список в Python. Плюсы и минусы:
    + простая реализация
    - медленная работа, т.к. операции с элементами списка имеют линейную сложность
    - неэффективное использование памяти, т.к. список может быть больше, чем нужно
'''

class FIFO2:
    def __init__(self, capacity):
        self.queue = deque(maxlen=capacity) # Создание очереди с заданным размером

    def is_full(self): # Проверка на заполненность
        return len(self.queue) == self.queue.maxlen

    def is_empty(self): # Проверка на пустоту
        return len(self.queue) == 0

    def enqueue(self, item): # Добавление элемента
        if self.is_full():
            # Опционально: можно обрабатывать переполнение
            self.queue.popleft()  # Удалить самый старый элемент, если нужно освободить место
        self.queue.append(item)

    def dequeue(self):  # Удаление элемента
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.queue.popleft()

    def peek(self): # Просмотр элемента
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.queue[0]
    
    def __str__(self):
        return str(list(self.queue))
    
'''Это реализация, использующая deque из collections. Плюсы и минусы:
    + быстрая работа, т.к. операции с элементами deque имеют константную сложность
    + эффективное использование памяти, т.к. deque использует только нужное количество памяти
    - сложнее реализация
    - не такой прямой контроль над функционалом 
    - зависимость от стандартной библиотеки

В целом для большинства задач лучше использовать вторую реализацию, т.к. она более эффективна и удобна в использовании.
'''

# Задание 3
'''На языке Python предложить алгоритм, который быстрее всего (по процессорным тикам) отсортирует данный ей массив чисел. 
Массив может быть любого размера со случайным порядком чисел (в том числе и отсортированным). 
Объяснить, почему вы считаете, что функция соответствует заданным критериям.'''

'''Во встроенной функции sort() используется timsort, который является наиболее оптимальным в большинстве случаев. Он реализован на низком уровне (на С),
а в худшем случае его сложность по времени составляет O(n log n). Таким образом, встроенная функция sort() является наиболее быстрой для сортировки массива чисел. 
Приведу реализацию алгоритма timsort на Python:'''

class TimSort:
    def insertion(self, arr, left=0, right=None): # Сортировка вставками
        if right is None:
            right = len(arr) - 1
        for i in range(left + 1, right + 1):
            key = arr[i]
            j = i - 1
            while j >= left and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    def merge(self, arr, left, mid, right): # Сортировка слиянием
        temp = []
        i, j = left, mid + 1
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp.append(arr[i])
                i += 1
            else:
                temp.append(arr[j])
                j += 1
        while i <= mid:
            temp.append(arr[i])
            i += 1
        while j <= right:
            temp.append(arr[j])
            j += 1
        for i, val in enumerate(temp):
            arr[left + i] = val

        return arr

    def timsort(self, arr): # сам timsort
        min_run = 32
        n = len(arr)

        for start in range(0, n, min_run):
            end = min(start + min_run - 1, n - 1)
            self.insertion(arr, start, end)

        size = min_run
        while size < n:
            for left in range(0, n, 2 * size):
                mid = min(n - 1, left + size - 1)
                right = min((left + 2 * size - 1), (n - 1))
                if mid < right:
                    self.merge(arr, left, mid, right)
            size *= 2

        return arr
    
    def timer(self, arr, func): #Вспомогательная функция для замера времени
        start = time.time()
        result = func(arr.copy())  
        end = time.time()
        print(f"{func.__name__} потратила {end - start} секунд.")
        return end-start
    
def main():
    sorter = TimSort()
    arr = [random.randint(0, 10000) for _ in range(10000)]
    nsertion_sort = sorter.timer(arr, sorter.insertion)
    timsort = sorter.timer(arr, sorter.timsort)
    # Сравнение времени работы алгоритмов. На массиве размером в 10000 timsort в среднем быстрее в 100 раз по сравнению с сортировкой вставками. 
    
if __name__ == "__main__":
    main()
