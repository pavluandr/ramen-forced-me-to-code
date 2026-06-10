class Node:
    """
    Узел связного списка для стека.
    
    Атрибуты:
        data: данные операции
        next (Node): ссылка на следующий узел
    """
    
    def __init__(self, data):
        """
        Конструктор узла стека.
        
        Аргументы:
            data: данные для хранения в узле
        """
        self.data = data
        self.next = None


class UndoStack:
    """
    Класс, реализующий стек на основе связного списка.
    Используется для хранения операций для отмены.
    """
    
    def __init__(self):
        """Конструктор стека. Создаёт пустой стек."""
        self.top = None
        self.size = 0
    
    def push(self, operation):
        """
        Добавляет операцию на вершину стека.
        
        Аргументы:
            operation: данные операции (словарь или кортеж)
        """
        new_node = Node(operation)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
    
    def pop(self):
        """
        Удаляет и возвращает операцию с вершины стека.
        
        Возвращает:
            данные операции или None, если стек пуст
        """
        if self.is_empty():
            return None
        
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data
    
    def peek(self):
        """
        Возвращает операцию с вершины стека без удаления.
        
        Возвращает:
            данные операции или None, если стек пуст
        """
        if self.is_empty():
            return None
        return self.top.data
    
    def is_empty(self):
        """
        Проверяет, пуст ли стек.
        
        Возвращает:
            bool: True если стек пуст, иначе False
        """
        return self.top is None
    
    def get_size(self):
        """
        Возвращает количество элементов в стеке.
        
        Возвращает:
            int: размер стека
        """
        return self.size