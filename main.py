from models import Expense
from storage import ExpenseTree
from analytics import PrefixSumArray, MaxExpenseFinder, CategorySorter
from undo_stack import UndoStack
from utils import (
    get_date_range_input,
    sync_prefix_sum_with_tree,
    print_separator,
    validate_amount,
    format_currency,
    get_validated_day_from_user,
)


class ExpenseTrackerApp:
    """
    Главный класс приложения. Управляет всеми компонентами и пользовательским интерфейсом.
    """
    
    def __init__(self):
        """Инициализация приложения: создание всех компонентов"""
        self.tree = ExpenseTree()           # Дерево для хранения расходов
        self.prefix_sum = PrefixSumArray()  # Префиксные суммы
        self.finder = MaxExpenseFinder()    # Поиск максимумов
        self.sorter = CategorySorter()      # Сортировка категорий
        self.undo_stack = UndoStack()       # Стек для отмены операций
        
        self.running = True                 # Флаг работы программы
    
    def run(self):
        """Главный цикл программы"""
        self._print_welcome()
        
        while self.running:
            self._print_menu()
            choice = self._get_choice()
            self._handle_choice(choice)
    
    def _print_welcome(self):
        """Приветственное сообщение"""
        print("\n" + "=" * 50)
        print("   ДОБРО ПОЖАЛОВАТЬ В ТРЕКЕР РАСХОДОВ!")
        print("=" * 50)
        print("\nПрограмма помогает отслеживать ежедневные расходы.")
        print("Вы можете добавлять траты, смотреть отчёты и отменять действия.\n")
    
    def _print_menu(self):
        """Выводит главное меню"""
        print_separator()
        print("\n📋 МЕНЮ:")
        print("   1. ➕ Добавить расход")
        print("   2. 📊 Показать сумму расходов за период")
        print("   3. 🔄 Отменить последнее действие")
        print("   4. 📈 Найти день с максимальным расходом")
        print("   5. 🏆 Найти максимальную отдельную покупку")
        print("   6. 📁 Показать отчёт по категориям")
        print("   7. 📅 Показать все расходы за месяц")
        print("   8. 📂 Загрузить данные из файла")
        print("   9. 🗑️  Очистить все данные")
        print("   10. 🚪 Выход")
        print_separator()
    
    def _get_choice(self):
        """Получает выбор пользователя"""
        while True:
            try:
                choice = int(input("\nВаш выбор: "))
                if 1 <= choice <= 10:
                    return choice
                else:
                    print("Ошибка: введите число от 1 до 10")
            except ValueError:
                print("Ошибка: введите целое число")
    
    def _handle_choice(self, choice):
        """Обрабатывает выбор пользователя"""
        if choice == 1:
            self._add_expense()
        elif choice == 2:
            self._show_range_sum()
        elif choice == 3:
            self._undo_last()
        elif choice == 4:
            self._show_max_day()
        elif choice == 5:
            self._show_max_expense()
        elif choice == 6:
            self._show_categories_report()
        elif choice == 7:
            self._show_all_expenses()
        elif choice == 8:
            self._load_from_file()
        elif choice == 9:
            self._clear_all_data()
        elif choice == 10:
            self._exit_app()
    
    def _add_expense(self):
        """Добавление нового расхода"""
        print("\n--- Добавление нового расхода ---")
        
        # Ввод дня
        day_input = input("Введите день (1-31) или дату (ГГГГ-ММ-ДД или ДД.ММ.ГГГГ): ")
        try:
            day = get_validated_day_from_user(day_input)
        except ValueError as e:
            print(f"Ошибка: {e}")
            return
        
        # Ввод суммы
        while True:
            try:
                amount = float(input("Введите сумму (руб.): "))
                if validate_amount(amount):
                    break
                else:
                    print("Ошибка: сумма должна быть положительным числом")
            except ValueError:
                print("Ошибка: введите число")
        
        # Ввод категории
        category = input("Введите категорию (например, 'Еда', 'Транспорт'): ").strip()
        if not category:
            category = "Прочее"
        
        # Создаём расход
        expense = Expense(day, amount, category)
        
        # Добавляем в дерево
        self.tree.insert(expense.day, expense)
        
        # Сохраняем операцию в стек для отмены
        operation = {
            'type': 'add',
            'expense': expense,
            'day': day,
            'amount': amount,
            'category': category
        }
        self.undo_stack.push(operation)
        
        # Обновляем префиксные суммы
        sync_prefix_sum_with_tree(self.tree, self.prefix_sum)
        
        print(f"\n✅ Расход добавлен: {expense}")
    
    def _show_range_sum(self):
        """Показывает сумму расходов за период"""
        if self.tree.is_empty():
            print("\n⚠️ Нет данных о расходах. Сначала добавьте расходы.")
            return
        
        day_a, day_b = get_date_range_input()
        
        try:
            total = self.prefix_sum.range_sum(day_a, day_b)
            print(f"\n💰 Сумма расходов с {day_a} по {day_b} день: {format_currency(total)}")
        except ValueError as e:
            print(f"\n❌ Ошибка: {e}")
    
    def _undo_last(self):
        """Отмена последнего действия"""
        operation = self.undo_stack.pop()
        
        if operation is None:
            print("\n⚠️ Нет действий для отмены")
            return
        
        if operation['type'] == 'add':
            expense = operation['expense']
            # Удаляем расход из дерева
            removed = self.tree.remove_expense(expense.day)
            if removed:
                print(f"\n✅ Отменено добавление: {expense}")
                # Обновляем префиксные суммы
                sync_prefix_sum_with_tree(self.tree, self.prefix_sum)
            else:
                print(f"\n❌ Не удалось отменить операцию")
    
    def _show_max_day(self):
        """Показывает день с максимальной суммой расходов"""
        if self.tree.is_empty():
            print("\n⚠️ Нет данных о расходах. Сначала добавьте расходы.")
            return
        
        daily_totals = self.tree.get_daily_totals_array()
        result = self.finder.find_max_day(daily_totals)
        
        if result is None:
            print("\n📊 Нет данных для анализа")
        else:
            day, amount = result
            print(f"\n📈 День с максимальными расходами: ДЕНЬ {day}")
            print(f"   Сумма: {format_currency(amount)}")
    
    def _show_max_expense(self):
        """Показывает максимальную отдельную покупку"""
        if self.tree.is_empty():
            print("\n⚠️ Нет данных о расходах. Сначала добавьте расходы.")
            return
        
        all_expenses = self.tree.get_all_expenses()
        result = self.finder.find_max_expense(all_expenses)
        
        if result is None:
            print("\n📊 Нет данных для анализа")
        else:
            expense, day = result
            print(f"\n🏆 Максимальная отдельная покупка:")
            print(f"   {expense}")
            print(f"   📅 День: {day}")
    
    def _show_categories_report(self):
        """Показывает отчёт по категориям (отсортированный)"""
        if self.tree.is_empty():
            print("\n⚠️ Нет данных о расходах. Сначала добавьте расходы.")
            return
        
        all_expenses = self.tree.get_all_expenses()
        sorted_categories = self.sorter.get_sorted_categories(all_expenses, reverse=True)
        self.sorter.print_categories(sorted_categories)
    
    def _show_all_expenses(self):
        """Показывает все расходы за месяц"""
        if self.tree.is_empty():
            print("\n⚠️ Нет данных о расходах. Сначала добавьте расходы.")
            return
        
        print("\n📅 ВСЕ РАСХОДЫ ЗА МЕСЯЦ:")
        print("-" * 40)
        
        all_expenses = self.tree.get_all_expenses()
        
        if not all_expenses:
            print("Нет расходов")
            return
        
        # Группируем по дням для красивого вывода
        expenses_by_day = {}
        for expense in all_expenses:
            if expense.day not in expenses_by_day:
                expenses_by_day[expense.day] = []
            expenses_by_day[expense.day].append(expense)
        
        # Выводим по дням
        for day in sorted(expenses_by_day.keys()):
            print(f"\n📆 ДЕНЬ {day}:")
            for expense in expenses_by_day[day]:
                print(f"   • {expense.category}: {format_currency(expense.amount)}")
            
            # Сумма за день
            day_total = sum(e.amount for e in expenses_by_day[day])
            print(f"   ───────────────────")
            print(f"   Итого за день: {format_currency(day_total)}")
        
        print_separator()
        
        # Общая сумма за месяц
        total_month = sum(e.amount for e in all_expenses)
        print(f"\n💰 ОБЩАЯ СУММА ЗА МЕСЯЦ: {format_currency(total_month)}")
    

    def _load_from_file(self):
        """Загружает расходы из файла"""
        print("\n--- Загрузка данных из файла ---")
    
        # Запрашиваем имя файла (с предложением стандартного)
        default_file = "expenses.txt"
        user_input = input(f"Введите имя файла (Enter для '{default_file}'): ").strip()
        
        filename = user_input if user_input else default_file
        
        try:
            from utils import load_expenses_from_file, get_data_file_path
            
            filepath = get_data_file_path(filename)
            expenses = load_expenses_from_file(filepath)
            
            if not expenses:
                print("⚠️ Файл пуст или не содержит валидных данных")
                return
            
            # Спрашиваем, как загружать
            print(f"\nНайдено {len(expenses)} расход(ов) в файле")
            print("Выберите режим загрузки:")
            print("   1. Добавить к существующим данным")
            print("   2. Очистить существующие и загрузить новые")
            
            mode = input("Ваш выбор (1/2): ").strip()
            
            if mode == '2':
                # Очищаем текущие данные
                self.tree = ExpenseTree()
                self.prefix_sum = PrefixSumArray()
                self.undo_stack = UndoStack()
                print("✅ Существующие данные очищены")
            
            # Загружаем расходы
            loaded_count = 0
            for expense in expenses:
                self.tree.insert(expense.day, expense)
                loaded_count += 1
                
                # Сохраняем каждую операцию в стек для возможной отмены
                operation = {
                    'type': 'add',
                    'expense': expense,
                    'day': expense.day,
                    'amount': expense.amount,
                    'category': expense.category
                }
                self.undo_stack.push(operation)
            
            # Обновляем префиксные суммы
            sync_prefix_sum_with_tree(self.tree, self.prefix_sum)
            
            print(f"\n✅ Успешно загружено {loaded_count} расход(ов) из файла '{filename}'")
            
            # Показываем краткую сводку
            daily_totals = self.tree.get_daily_totals_array()
            total = sum(daily_totals)
            print(f"💰 Общая сумма загруженных расходов: {format_currency(total)}")
            
        except FileNotFoundError:
            print(f"\n❌ Файл '{filename}' не найден в папке 'data/'")
            print("   Убедитесь, что файл существует и находится в правильной папке")
        except ValueError as e:
            print(f"\n❌ Ошибка в файле: {e}")
        except Exception as e:
            print(f"\n❌ Непредвиденная ошибка: {e}")

    
    def _clear_all_data(self):
        """Очистка всех данных"""
        print("\n⚠️ ВНИМАНИЕ: Это действие удалит все расходы!")
        confirm = input("Вы уверены? (да/нет): ").lower()
        
        if confirm == 'да' or confirm == 'yes' or confirm == 'y':
            self.tree = ExpenseTree()
            self.prefix_sum = PrefixSumArray()
            self.undo_stack = UndoStack()
            print("\n✅ Все данные очищены")
        else:
            print("\n❌ Очистка отменена")
    
    def _exit_app(self):
        """Выход из программы"""
        print("\n👋 До свидания! Хорошего дня!")
        self.running = False


def main():
    """Точка входа в программу"""
    app = ExpenseTrackerApp()
    app.run()


if __name__ == "__main__":
    main()