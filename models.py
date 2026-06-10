class Expense:
    """
    Информация об отдельной трате пользователя
    
    Attributes:
        day (int) - номер дня месяца от 1 до 31, когда произошла трата
        amount (int/float) - сумма траты
        category (str) - категории траты, например "Еда", "Спорт"
    
    Methods:
        __init__ - инициализария объекта
        __str__ - вывод информации об бъекте
    """

    def __init__(self, day, amount, category):
        """Инициализация объекта"""
        self.day = day
        self.amount = amount 
        self.category = category
    
    def __str__(self):
        """Возвращает удобочитаемую строку для вывода пользователю. Пример: 'День 5: Еда — 250.50 руб.' """
        return f'День {self.day}: {self.category} - {self.amount} руб.'

class Category:
    """
    Используется только для отчёта — сортировки категорий по сумме трат. 
    Не хранится в основном дереве, а создаётся на лету при запросе сортировки.
    
    Attributes:
        name (str) — название категории (например, "Еда")
        total_amount (float) — общая сумма всех трат по этой категории за месяц

    Methods:
        __init__(self, name, total_amount) — конструктор
        __lt__(self, other) — метод сравнения для сортировки вставками (сравнивает total_amount, чтобы сортировать по убыванию или возрастанию)
        __str__(self) — для вывода: "Категория 'Еда': 1250.80 руб."
    """

    def __init__(self, name, total_amount):
        """Инициализация объекта"""
        self.name = name
        self.total_amount = total_amount

    def __lt__(self, other):
        """Сравнивает значения двух объектов класса (строго меньше)"""
        return self.total_amount < other.total_amount
    
    def __str__(self):
        """Вывод в формате "Категория 'Еда': 1250.80 руб." """
        return f'Категория \'{self.name}\': {self.total_amount} руб.'
    
class DayExpense:
    """
    Представляет узел в бинарном дереве поиска. 
    Хранит все траты, сделанные в конкретный день, и ссылки на соседние дни (левое/правое поддерево).
    
    Attributes:
        day (int) - номер дня (ключ дерева)
        expenses (list) - коллекция объектов Expense за этот день
        left (объект DayExpense или None) - ссылка на узел с меньшим днем (левое поддерево)
        right (объект DayExpense или None) - ссылка на узел с большим днем (правое поддерево)
    
    Methods:
        __init__(self, day, expense) — конструктор, создаёт пустой список расходов
        add_expense(self, expense) — добавляет объект Expense в список expenses
        get_total_for_day(self) — возвращает сумму всех трат за этот день
        __str__(self) — возвращает "День 5: 2 траты на сумму 300.50 руб."
    """

    def __init__(self, day):
        """Инициализация пустого списка расходов"""
        self.day = day
        self.expenses = []
        self.left = None
        self.right = None
    
    def add_expense(self, expense):
        """Добавляет объект класса Expence в список трат"""
        self.expenses.append(expense)
    
    def get_total_for_day(self):
        """Возвращает сумму всех трат за день"""
        total_for_day = 0
        for expense in self.expenses:
            total_for_day += expense.amount
        
        return total_for_day
    
    def __str__(self):
        """Вывод в формате "День 5: 2 траты на сумму 300.50 руб." """
        count = len(self.expenses)
        if count % 10 == 1 and count % 100 != 11:
            word = 'трата'
        elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
            word = 'траты'
        else:
            word = 'трат'
        return f'День {self.day}: {count} {word} на сумму {self.get_total_for_day()} руб.'