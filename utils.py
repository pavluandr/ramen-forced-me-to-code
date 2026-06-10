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
        day_a = get_day_input("Введите день A (начало периода): ")
        day_b = get_day_input("Введите день В (конец периода): ")
        
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



def extract_day_from_date(date_string):
    """
    Извлекает номер дня из строки с датой.
    Поддерживает форматы: YYYY-MM-DD и DD.MM.YYYY
    """
    if '-' in date_string:
        return int(date_string.split('-')[2])
    elif '.' in date_string:
        return int(date_string.split('.')[0])
    else:
        raise ValueError(f"Неизвестный формат даты: {date_string}")


def try_parse_date(user_input):
    """
    Пробует преобразовать ввод пользователя в день.
    Возвращает: (день, успех или нет)
    """
    if user_input.isdigit():
        day = int(user_input)
        return day, validate_day(day)
    else:
        try:
            day = extract_day_from_date(user_input)
            return day, validate_day(day)
        except ValueError:
            return None, False


def get_validated_day_from_user(user_input):
    """Возвращает валидный день или выбрасывает исключение"""
    day, is_valid = try_parse_date(user_input)
    if is_valid:
        return day
    else:
        raise ValueError(f"'{user_input}' не является корректным днём (1-31) или датой")
    

def load_expenses_from_file(filepath):
    """
    Загружает расходы из текстового файла.
    
    Формат файла: каждая строка содержит "день,сумма,категория"
    Пример: "5,250.50,Еда"
    
    Arguments:
        filepath (str) - путь к файлу
    
    Returns:
        list[Expense] - список объектов Expense
    
    Exceptions:
        FileNotFoundError - если файл не найден
        ValueError - если данные в файле некорректны
    """
    from models import Expense
    
    expenses = []
    line_number = 0
    
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            line_number += 1
            line = line.strip()
            
            if not line:
                continue
            
            # Разделяем строку
            parts = line.split(',')
            if len(parts) != 3:
                raise ValueError(f"Ошибка в строке {line_number}: ожидается 3 значения (день,сумма,категория)")
            
            try:
                day = int(parts[0])
                amount = float(parts[1])
                category = parts[2].strip()
                
                # Валидация данных
                if not validate_day(day):
                    raise ValueError(f"День {day} должен быть от 1 до 31")
                if not validate_amount(amount):
                    raise ValueError(f"Сумма {amount} должна быть положительной")
                if not category:
                    category = "Прочее"
                
                expense = Expense(day, amount, category)
                expenses.append(expense)
                
            except ValueError as e:
                raise ValueError(f"Ошибка в строке {line_number}: {e}")
    
    return expenses


def get_data_file_path(filename="expenses.txt"):
    """
    Возвращает путь к файлу с данными.
    
    Arguments:
        filename (str) - имя файла
    
    Returns:
        str - полный путь к файлу
    """
    import os
    # Предполагаем, что файл лежит в папке data рядом с программой
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "data", filename)