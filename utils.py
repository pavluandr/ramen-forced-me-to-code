def validate_day(day):
    """
    Функция проверяет, является ли число допустимым днём месяца.
    
    Аргументы:
        day (int): число для проверки
        
    Возвращает:
        bool: True если день от 1 до 31, иначе False
    """
    return isinstance(day, int) and 1 <= day <= 31



def validate_amount(amount):
    """
    Функция проверяет, является ли сумма положительным числом.
    
    Аргументы:
        amount (float или int): сумма для проверки
        
    Возвращает:
        bool: True если сумма > 0, иначе False
    """
    return isinstance(amount, (int, float)) and amount > 0



def format_currency(value):
    """
    Функция форматирует число как денежную сумму.
    
    Аргументы:
        value (float или int): сумма
        
    Возвращает:
        str: отформатированная строка
    """
    return f"{value:.2f} руб."



def get_day_input(prompt):
    """
    Функция запрашивает у пользователя номер дня с проверкой.
    
    Аргументы:
        prompt (str): текст приглашения для ввода
        
    Возвращает:
        int: корректный номер дня
    """
    while True:
        try:
            day = int(input(prompt))
            if validate_day(day):
                return day
            else:
                print("Ошибка: день должен быть от 1 до 31. Попробуйте снова")
        except ValueError:
            print("Ошибка: введите целое число")
            
            
            
def get_date_range_input():
    """
    Функция запрашивает у пользователя диапазон дней (A и B) с проверкой.
    
    Возвращает:
        tuple (int, int): (day_a, day_b) где day_a <= day_b
    """
    print("\n--- Запрос суммы за период ---")
    
    while True:
        day_a = get_day_input("Введите в день A (начало периода): ")
        day_b = get_day_input("Введите в день В (конец периода): ")
        
        if day_a <= day_b:
            return (day_a, day_b)
        else:
            print("Ошибка: день А должен быть меньше или равен дню В. Попробуйте снова.")
            

def get_all_expenses_summary(tree):
    """
    Функция собирает массив сумм по дням из дерева.
    
    Аргументы:
        tree (ExpenseTree): объект дерева расходов
        
    Возвращает:
        list: массив из 32 элементов (индексы 0-31, индекс 0 не используется)
    """
    # Создаём массив на 32 элемента (индекс 0 не используем)
    daily_totals = [0.0] * 32
    
    # Получаем все расходы из дерева
    all_expenses = tree.get_all_expenses()
    
    # Суммируем расходы по дням
    for expense in all_expenses:
        daily_totals[expense.day] += expense.amount
    
    return daily_totals



def sync_prefix_sum_with_tree(tree, prefix_sum_obj):
    """
    Функция обновляет префиксный массив на основе данных из дерева.
    
    Аргументы:
        tree (ExpenseTree): объект дерева расходов
        prefix_sum_obj (PrefixSumArray): объект префиксного массива
    """
    daily_totals = get_all_expenses_summary(tree)
    prefix_sum_obj.build(daily_totals)
    
    
    
def print_separator():
    """
    Функция выводит разделительную линию для интерфейса.
    
    """
    print("-" * 50)




















































































































































