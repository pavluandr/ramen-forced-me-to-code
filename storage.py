"""
storage.py - реализация бинарного дерева поиска для хранения расходов по дням
"""

from models import DayExpense, Expense


class ExpenseTree:
    """
    Класс, реализующий бинарное дерево поиска для хранения расходов.
    Ключ дерева - номер дня (int).
    """
    
    def __init__(self):
        """Конструктор дерева. Создаёт пустое дерево."""
        self.root = None
        self.size = 0
    
    def insert(self, day, expense):
        """
        Добавляет расход в дерево.
        Если день уже существует, добавляет трату в существующий узел.
        Если дня нет, создаёт новый узел.
        
        Аргументы:
            day (int): номер дня
            expense (Expense): объект траты
        """
        if self.root is None:
            # Дерево пустое - создаём корневой узел
            self.root = DayExpense(day)
            self.root.add_expense(expense)
            self.size += 1
        else:
            self._insert_recursive(self.root, day, expense)
    
    def _insert_recursive(self, node, day, expense):
        """
        Рекурсивная вставка узла в дерево.
        
        Аргументы:
            node (DayExpense): текущий узел
            day (int): номер дня
            expense (Expense): объект траты
        """
        if day == node.day:
            # День найден - добавляем трату в существующий узел
            node.add_expense(expense)
        elif day < node.day:
            # Идём в левое поддерево
            if node.left is None:
                node.left = DayExpense(day)
                node.left.add_expense(expense)
                self.size += 1
            else:
                self._insert_recursive(node.left, day, expense)
        else:
            # Идём в правое поддерево (day > node.day)
            if node.right is None:
                node.right = DayExpense(day)
                node.right.add_expense(expense)
                self.size += 1
            else:
                self._insert_recursive(node.right, day, expense)
    
    def find(self, day):
        """
        Ищет узел с указанным днём.
        
        Аргументы:
            day (int): номер дня для поиска
            
        Возвращает:
            DayExpense: узел с тратами за день или None, если день не найден
        """
        return self._find_recursive(self.root, day)
    
    def _find_recursive(self, node, day):
        """
        Рекурсивный поиск узла в дереве.
        
        Аргументы:
            node (DayExpense): текущий узел
            day (int): номер дня для поиска
            
        Возвращает:
            DayExpense: найденный узел или None
        """
        if node is None:
            return None
        
        if day == node.day:
            return node
        elif day < node.day:
            return self._find_recursive(node.left, day)
        else:
            return self._find_recursive(node.right, day)
    
    def remove_expense(self, day, expense_index=None):
        """
        Удаляет расход из указанного дня.
        Если после удаления список расходов дня пуст, удаляет узел из дерева.
        
        Аргументы:
            day (int): номер дня
            expense_index (int, optional): индекс удаляемой траты.
                                          Если None, удаляет последнюю трату.
                                          
        Возвращает:
            Expense: удалённая трата или None, если удалить не удалось
        """
        node = self.find(day)
        if node is None:
            return None
        
        # Определяем, какую трату удалять
        if expense_index is None and len(node.expenses) > 0:
            # Удаляем последнюю трату
            removed_expense = node.expenses.pop()
        elif expense_index is not None and 0 <= expense_index < len(node.expenses):
            removed_expense = node.expenses.pop(expense_index)
        else:
            return None
        
        # Если после удаления в узле не осталось трат, удаляем узел из дерева
        if len(node.expenses) == 0:
            self._delete_node(day)
        
        return removed_expense
    
    def _delete_node(self, day):
        """
        Удаляет узел с указанным днём из дерева.
        
        Аргументы:
            day (int): номер дня для удаления
        """
        self.root = self._delete_recursive(self.root, day)
    
    def _delete_recursive(self, node, day):
        """
        Рекурсивное удаление узла из дерева.
        
        Аргументы:
            node (DayExpense): текущий узел
            day (int): номер дня для удаления
            
        Возвращает:
            DayExpense: новый корень поддерева после удаления
        """
        if node is None:
            return None
        
        if day < node.day:
            node.left = self._delete_recursive(node.left, day)
        elif day > node.day:
            node.right = self._delete_recursive(node.right, day)
        else:
            # Нашли узел для удаления
            
            # Случай 1: нет детей
            if node.left is None and node.right is None:
                self.size -= 1
                return None
            
            # Случай 2: один ребёнок
            if node.left is None:
                self.size -= 1
                return node.right
            if node.right is None:
                self.size -= 1
                return node.left
            
            # Случай 3: два ребёнка
            # Находим минимальный узел в правом поддереве
            successor = self._find_min(node.right)
            # Копируем данные из преемника в текущий узел
            node.day = successor.day
            node.expenses = successor.expenses
            # Удаляем преемника
            node.right = self._delete_recursive(node.right, successor.day)
        
        return node
    
    def _find_min(self, node):
        """
        Находит узел с минимальным днём в поддереве.
        
        Аргументы:
            node (DayExpense): корень поддерева
            
        Возвращает:
            DayExpense: узел с минимальным днём
        """
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def get_all_expenses(self):
        """
        Возвращает список всех расходов из дерева (симметричный обход).
        
        Возвращает:
            list: список всех объектов Expense
        """
        all_expenses = []
        self._inorder_traversal(self.root, all_expenses)
        return all_expenses
    
    def _inorder_traversal(self, node, result_list):
        """
        Рекурсивный симметричный обход дерева.
        
        Аргументы:
            node (DayExpense): текущий узел
            result_list (list): список для сбора результатов
        """
        if node is not None:
            # Левое поддерево
            self._inorder_traversal(node.left, result_list)
            
            # Текущий узел (добавляем все траты этого дня)
            for expense in node.expenses:
                result_list.append(expense)
            
            # Правое поддерево
            self._inorder_traversal(node.right, result_list)
    
    def get_daily_totals_array(self):
        """
        Возвращает массив сумм по дням (индекс = день, значение = сумма).
        
        Возвращает:
            list: массив из 32 элементов (индексы 0-31, индекс 0 не используется)
        """
        daily_totals = [0.0] * 32
        self._collect_daily_totals(self.root, daily_totals)
        return daily_totals
    
    def _collect_daily_totals(self, node, totals_array):
        """
        Рекурсивный сбор сумм по дням.
        
        Аргументы:
            node (DayExpense): текущий узел
            totals_array (list): массив для заполнения сумм
        """
        if node is not None:
            self._collect_daily_totals(node.left, totals_array)
            totals_array[node.day] = node.get_total_for_day()
            self._collect_daily_totals(node.right, totals_array)
    
    def display_tree(self):
        """
        Выводит дерево в консоль (для отладки).
        """
        self._display_recursive(self.root, 0)
    
    def _display_recursive(self, node, level):
        """
        Рекурсивный вывод дерева с отступами.
        
        Аргументы:
            node (DayExpense): текущий узел
            level (int): уровень вложенности
        """
        if node is not None:
            self._display_recursive(node.right, level + 1)
            print("    " * level + f"День {node.day}: {len(node.expenses)} трат(ы), сумма: {node.get_total_for_day():.2f} руб.")
            self._display_recursive(node.left, level + 1)
    
    def get_size(self):
        """
        Возвращает количество дней с расходами.
        
        Возвращает:
            int: количество узлов в дереве
        """
        return self.size
    
    def is_empty(self):
        """
        Проверяет, пустое ли дерево.
        
        Возвращает:
            bool: True если дерево пустое, иначе False
        """
        return self.root is None
