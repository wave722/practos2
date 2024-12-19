import sys

# Данные приложения
menu = [
    {"id": 1, "name": "Салат Цезарь", "price": 350, "category": "Салаты", "rating": 4.7},
    {"id": 2, "name": "Борщ", "price": 250, "category": "Супы", "rating": 4.5},
    {"id": 3, "name": "Филе-миньон", "price": 1200, "category": "Основные блюда", "rating": 4.9},
]

users = [
    {"username": "guest_user", "password": "guest123", "role": "user", "order_history": []},
    {"username": "admin", "password": "admin", "role": "admin"},
]

orders = []

# Авторизация пользователя
def login(users):
    username = input("Введите логин: ")
    password = input("Введите пароль: ")
    for user in users:
        if user['username'] == username and user['password'] == password:
            print(f"Добро пожаловать, {username}!")
            return user
    print("Неверный логин или пароль.")
    return None

# Просмотр меню
def view_menu(menu):
    print("\nМеню ресторана:")
    print(f"{'ID':<5}{'Название':<20}{'Цена':<10}{'Категория':<15}{'Рейтинг':<10}")
    for dish in menu:
        print(f"{dish['id']:<5}{dish['name']:<20}{dish['price']:<10}{dish['category']:<15}{dish['rating']:<10.1f}")

# Создание заказа
def create_order(user, menu, orders):
    order_items = []
    total_cost = 0
    while True:
        view_menu(menu)
        dish_id = input("Введите ID блюда для добавления в заказ (или '0' для завершения): ")
        if dish_id == '0':
            break
        for dish in menu:
            if dish['id'] == int(dish_id):
                order_items.append(dish['name'])
                total_cost += dish['price']
                print(f"Добавлено: {dish['name']} ({dish['price']} руб.)")
                break
        else:
            print("Блюдо с таким ID не найдено.")

    if order_items:
        order = {"order_id": len(orders) + 1, "user": user['username'], "items": order_items, "total": total_cost, "date": "2024-12-14"}
        orders.append(order)
        user['order_history'].append(order)
        print(f"Заказ создан! Общая стоимость: {total_cost} руб.")
    else:
        print("Заказ пуст.")

# Сортировка блюд
def sort_menu(menu):
    criterion = input("Введите критерий сортировки (price/rating): ")
    if criterion == "price":
        sorted_menu = sorted(menu, key=lambda x: x['price'])
    elif criterion == "rating":
        sorted_menu = sorted(menu, key=lambda x: x['rating'], reverse=True)
    else:
        print("Неверный критерий.")
        return
    view_menu(sorted_menu)

# Фильтрация блюд
def filter_menu(menu):
    category = input("Введите категорию для фильтрации: ")
    filtered_menu = list(filter(lambda x: x['category'] == category, menu))
    if filtered_menu:
        view_menu(filtered_menu)
    else:
        print("Нет блюд в данной категории.")

# Проверка ввода для числовых значений
def validate_input(prompt, value_type, min_value=None, max_value=None):
    while True:
        try:
            value = value_type(input(prompt))
            if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                print(f"Введите значение от {min_value} до {max_value}.")
                continue
            return value
        except ValueError:
            print("Неверный ввод. Попробуйте снова.")

# Главный цикл пользователя
def user_menu(user):
    while True:
        print("\nВыберите действие:")
        print("1. Просмотреть меню")
        print("2. Найти блюда по категории")
        print("3. Сортировать блюда")
        print("4. Создать заказ")
        print("5. Посмотреть историю заказов")
        print("6. Выйти")
        choice = input("Ваш выбор: ")

        if choice == '1':
            view_menu(menu)
        elif choice == '2':
            filter_menu(menu)
        elif choice == '3':
            sort_menu(menu)
        elif choice == '4':
            create_order(user, menu, orders)
        elif choice == '5':
            print("\nИстория заказов:")
            for order in user['order_history']:
                print(order)
        elif choice == '6':
            print("До свидания!")
            break
        else:
            print("Неверный выбор.")
# Главный цикл администратора
def admin_menu():
    global menu  # Объявляем меню глобальным, чтобы изменения сохранялись
    while True:
        print("\nВыберите действие:")
        print("1. Добавить блюдо")
        print("2. Удалить блюдо")
        print("3. Редактировать блюдо")
        print("4. Просмотреть заказы")
        print("5. Выйти")
        choice = input("Ваш выбор: ")

        if choice == '1':
            name = input("Название блюда: ")
            price = validate_input("Цена: ", int, 0)
            category = input("Категория: ")
            rating = validate_input("Рейтинг: ", float, 0.0, 5.0)
            new_dish = {"id": len(menu) + 1, "name": name, "price": price, "category": category, "rating": rating}
            menu.append(new_dish)
            print("Блюдо добавлено!")
            view_menu(menu)  # Показываем актуализированное меню
        elif choice == '2':
            # Перед удалением выводим актуальное меню
            print("\nТекущее меню:")
            view_menu(menu)
            dish_id = validate_input("Введите ID блюда для удаления: ", int, 1)
            menu = [dish for dish in menu if dish['id'] != dish_id]  # Обновляем список меню
            print("Блюдо удалено!")
            view_menu(menu)  # Показываем актуализированное меню
        elif choice == '3':
            # Перед редактированием выводим актуальное меню
            print("\nТекущее меню:")
            view_menu(menu)
            dish_id = validate_input("Введите ID блюда для редактирования: ", int, 1)
            for dish in menu:
                if dish['id'] == dish_id:
                    dish['name'] = input(f"Название ({dish['name']}): ") or dish['name']
                    dish['price'] = validate_input(f"Цена ({dish['price']}): ", int, 0)
                    dish['category'] = input(f"Категория ({dish['category']}): ") or dish['category']
                    dish['rating'] = validate_input(f"Рейтинг ({dish['rating']}): ", float, 0.0, 5.0)
                    print("Блюдо обновлено!")
                    view_menu(menu)  # Показываем актуализированное меню
                    break
            else:
                print("Блюдо не найдено.")
        elif choice == '4':
            print("\nСписок заказов:")
            for order in orders:
                print(order)
        elif choice == '5':
            print("До свидания!")
            break
        else:
            print("Неверный выбор.")

# Точка входа
if __name__ == "__main__":
    print("Добро пожаловать в ресторан!")
    user = None
    while not user:
        user = login(users)

    if user['role'] == "user":
        user_menu(user)
    elif user['role'] == "admin":
        admin_menu()
