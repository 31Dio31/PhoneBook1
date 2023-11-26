import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('справочник.db')
cursor = conn.cursor()

# Создание таблицы, если она не существует
query = '''CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT
)'''
cursor.execute(query)
conn.commit()

# Функции для команд
def display_contacts():
    print("Телефонный справочник:")
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    for contact in contacts:
        print(f"ID: {contact[0]}, Имя: {contact[1]}, Телефон: {contact[2]}, Email: {contact[3]}")
    print()

def add_contact():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    email = input("Введите email: ")
    query = "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)"
    cursor.execute(query, (name, phone, email))
    conn.commit()
    print("Контакт успешно добавлен!")
    print()

def search_contact():
    keyword = input("Введите имя или телефон для поиска: ")
    query = "SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?"
    cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
    contacts = cursor.fetchall()
    if contacts:
        print("Результаты поиска:")
        for contact in contacts:
            print(f"ID: {contact[0]}, Имя: {contact[1]}, Телефон: {contact[2]}, Email: {contact[3]}")
    else:
        print("Контакты не найдены")
    print()

def delete_contact():
    contact_id = input("Введите ID контакта для удаления: ")
    query = "DELETE FROM contacts WHERE id = ?"
    cursor.execute(query, (contact_id,))
    conn.commit()
    print("Контакт успешно удален!")
    print()

def update_contact():
    contact_id = input("Введите ID контакта для обновления: ")
    name = input("Введите новое имя: ")
    phone = input("Введите новый телефон: ")
    email = input("Введите новый email: ")
    query = "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?"
    cursor.execute(query, (name, phone, email, contact_id))
    conn.commit()
    print("Контакт успешно обновлен!")
    print()

def import_contacts():
    filename = input("Введите название файла для импорта: ")
    try:
        with open(filename, "r") as file:
            for line in file:
                name, phone, email = line.strip().split(",")
                query = "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)"
                cursor.execute(query, (name, phone, email))
        conn.commit()
        print("Контакты успешно импортированы!")
    except FileNotFoundError:
        print("Файл не найден")
    print()

# Главное меню приложения
while True:
    print("1. Просмотреть контакты")
    print("2. Добавить контакт")
    print("3. Поиск контакта")
    print("4. Удалить контакт")
    print("5. Обновить контакт")
    print("6. Импортировать контакты из файла")
    print("0. Выход")
    choice = input("Выберите действие: ")

    if choice == "1":
        display_contacts()
    elif choice == "2":
        add_contact()
    elif choice == "3":
        search_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        update_contact()
    elif choice == "6":
        import_contacts()
    elif choice == "0":
        break
    else:
        print("Некорректный выбор. Попробуйте снова")
        print()

# Закрытие соединения с базой данных
conn.close()