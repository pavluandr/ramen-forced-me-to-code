from models import Category

class PrefixSumArray:
    """
    Хранит массив префиксных сумм расходов по дням и отвечает на запросы суммы за период за O(1)

    Attributes:
        prefix_sum (list of float) - массив префиксных сумм из 32 элементов
    
    Methods:
        __init__(self) - создает пустой массив из 32 нулей
        build(self, daily_totals) - строит массив префиксных сумм
        range_sum(self, day_a, day_b) - подсчитываем сумму расходов с дня А по день B
        __str__(self) - выводит первые 10 элементов префиксного массива (преймущественно для отладки)
    """

    def __init__(self):
        """Создание пустого массива из 32 нулей"""
        self.prefix_sum = [0.0] * 32
    
    def build(self, daily_totals):
        """
        Создание массива префиксных сумм на основе массива трат
        
        Arguments:
            daily_totals (list of int/float) - список трат по дням из целых чисел или чисел с плавующей точкой
        """
        running_sum = 0.0
        for day in range(1, 32):
            running_sum += daily_totals[day]
            self.prefix_sum[day] = running_sum

    def range_sum(self, day_a, day_b):
        """
        Подсчет суммы расходов с дня А по день В включительно. Если дни равны, то сумма за один день
        
        Arguments:
            day_a - первый день (число от 1 до 31)
            day_b - второй день(число от 1 до 31)
        """
        if day_a > day_b:
            raise ValueError("Должно соблюдаться неравенство: day_a <= day_b")
    
        return self.prefix_sum[day_b] - self.prefix_sum[day_a - 1]

    def __str__(self):
        """Вывод первых 10 элементов массива префиксов в виде списка"""
        elements = [str(x) for x in self.prefix_sum[:10]]
        return f'[{", ".join(elements)}]'

class MaxExpenseFinder:
    """
    Выполняет линейный поиск дня с максимальной суммой расходов. 
    Нет постоянных атрибутов — класс работает как сервис (набор методов без хранения состояния)
    
    Methods:
        find_max_day(self, daily_totals) - найти день с максимальной суммой
        find_max_expense(self, expenses_list) - ищет максимальную отдельную покупку
    """

    def find_max_day(self, daily_totals):
        """
        Проходит по всем дням (1-31), находит день с максимальной суммой. Возвращает (день, сумма). Если все суммы = 0, возвращает None.
        
        Arguments:
            daily_totals (list of int/float) - список трат из целых чисел или чисел с плавующей точкой
        
        Returns:
            tuple(int, float) или None - массив вида (день, суммарная_трата) для дня с максимальными тратами
        """
        current_max = 0
        max_day = None
        for day in range(daily_totals):
            if daily_totals[day] > current_max:
                current_max = daily_totals[day]
                max_day = day + 1
        return (max_day) if max_day != None else None

    def find_max_expense(self, expenses_list):
        """
        Ищет максимальную отдельную покупку (объект Expense с наибольшей суммой).
        
        Arguments:
            expenses_list (list[Expense]): список всех объектов Expense из дерева
        
        Returns:
            tuple (Expense, int) or None: (объект_расхода, день) или None, если список пуст
        """
        if not expenses_list:
            print("Список расходов пуст")
            return None
        
        max_expense = expenses_list[0]
        
        for expense in expenses_list[1:]:
            if expense.amount > max_expense.amount:
                max_expense = expense
        
        return (max_expense, max_expense.day)

class CategorySorter:
    """
    Агрегирует расходы по категориям и сортирует их методом вставок.
    Нет постоянных атрибутов — класс работает как сервис (набор методов без хранения состояния)

    Methods:
        aggregate_by_category(self, expenses_list) - суммировать расходы по категориям
    """
    
    def aggregate_by_category(self, expenses_list):
        """
        Суммирует расходы по категориям.
        
        Arguments:
            expenses_list (list[Expense]) - список всех расходов
        
        Returns:
            dict - словарь {категория: общая_сумма}
        """
        category_totals = {}
        
        for expense in expenses_list:
            if expense.category in category_totals:
                category_totals[expense.category] += expense.amount
            else:
                category_totals[expense.category] = expense.amount
        
        return category_totals
    
    def dict_to_category_list(self, category_dict):
        """
        Преобразует словарь в список объектов Category.
        
        Arguments:
            category_dict (dict): словарь {категория: сумма}
        
        Returns:
            list[Category]: список объектов Category
        """
        categories = []
        
        for name, total in category_dict.items():
            categories.append(Category(name, total))
        
        return categories
    
    def insertion_sort(self, categories_list, reverse=True):
        """
        Сортирует список категорий методом вставок.
        
        Arguments:
            categories_list (list[Category]): список для сортировки
            reverse (bool): True — по убыванию, False — по возрастанию
        
        Returns:
            list[Category]: отсортированный список (сортирует на месте)
        """
        n = len(categories_list)
        
        for i in range(1, n):
            key = categories_list[i]
            j = i - 1
            
            if reverse:
                # Сортировка по убыванию
                while j >= 0 and categories_list[j].total_amount < key.total_amount:
                    categories_list[j + 1] = categories_list[j]
                    j -= 1
            else:
                # Сортировка по возрастанию
                while j >= 0 and categories_list[j].total_amount > key.total_amount:
                    categories_list[j + 1] = categories_list[j]
                    j -= 1
            
            categories_list[j + 1] = key
        
        return categories_list
    
    def get_sorted_categories(self, expenses_list, reverse=True):
        """
        Агрегирует и сортирует категории за один вызов.
        
        Arguments:
            expenses_list (list[Expense]) - список всех расходов
            reverse (bool) : True — по убыванию, False — по возрастанию
        
        Returns:
            list[Category] - отсортированный список категорий
        """
        # Агрегируем суммы по категориям
        category_dict = self.aggregate_by_category(expenses_list)
        
        # Преобразуем в список объектов Category
        categories = self.dict_to_category_list(category_dict)
        
        # Сртируем вставками
        self.insertion_sort(categories, reverse)
        
        return categories
    
    def print_categories(self, categories_list):
        """
        Выводит список категорий.
        
        Arguments:
            categories_list (list[Category]) - список категорий
        """
        if not categories_list:
            print("Нет данных по категориям")
            return
        
        print("\n=== Расходы по категориям ===")
        for i, category in enumerate(categories_list, 1):
            print(f"{i}. {category}")
        print("=" * 30)