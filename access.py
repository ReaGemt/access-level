import tkinter as tk
from tkinter import messagebox

# Создаем класс пользователя
class User:
    def __init__(self, user_id, name, password):
        self.__user_id = user_id
        self.__name = name
        self.__access_level = 'Пользователь'
        self.__password = password

    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_access_level(self):
        return self.__access_level

    def set_name(self, name):
        self.__name = name

    def check_password(self, password):
        return self.__password == password

    def set_password(self, new_password):
        self.__password = new_password

    def __str__(self):
        return f'ID Пользователя: {self.__user_id}, Имя: {self.__name}, Уровень доступа: {self.__access_level})'

# Создаем класс администратора Admin наследует от User и имеет дополнительный атрибут __access_level,
# который указывает на уровень доступа администратора.
class Admin(User):
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)
        self.__access_level = 'Администратор'

    def add_user(self, user_list, user):
        user_list.append(user)

    def remove_user(self, user_list, user_id):
        user_list[:] = [user for user in user_list if user.get_user_id() != user_id]

    def get_access_level(self):
        return self.__access_level

    def __str__(self):
        return f'ID Администратора: {self.get_user_id()}, Имя: {self.get_name()}, Уровень доступа: {self.__access_level})'

# Создаем список, который будет содержать всех пользователей, включая администраторов
user_list = []

# Создаем администратора
admin = Admin(1, 'Алексей', '12345')

# Создаем обычных пользователей
user1 = User(2, 'Ирина', '123')
user2 = User(3, 'Пётр', '456')

# Администратор добавляет пользователей
admin.add_user(user_list, user1)
admin.add_user(user_list, user2)
# Добавляем администратора в список пользователей
user_list.append(admin)


# Функция для приветственного окна
def show_welcome_window(user_name, access_level):
    welcome_window = tk.Toplevel(app)
    welcome_window.title("Авторизация")
    welcome_window.geometry("300x200")  # Устанавливаем начальный размер окна
    welcome_window.resizable(True, True)  # Разрешаем изменение размеров окна

    welcome_label = tk.Label(welcome_window, text=f"Добро пожаловать, {user_name}!\nВаш уровень доступа: {access_level}")
    welcome_label.pack(padx=20, pady=20)

    ok_button = tk.Button(welcome_window, text="Подтвердить", command=welcome_window.destroy)
    ok_button.pack(pady=10)

    if access_level == 'Администратор':
        manage_users_button = tk.Button(welcome_window, text="Управление пользователями", command=manage_users_window)
        manage_users_button.pack(pady=10)


# Функция для управления пользователями (доступно только администратору)
def manage_users_window():
    manage_window = tk.Toplevel()
    manage_window.title("Управление пользователями")
    manage_window.geometry("500x600")
    manage_window.resizable(True, True)

    # Метка для заголовка списка пользователей
    tk.Label(manage_window, text="Список пользователей", font=("Helvetica", 16)).pack(pady=10)

    # Создаем текстовое поле для вывода списка пользователей
    users_text = tk.Text(manage_window, height=10, width=50)
    users_text.pack(padx=20, pady=10)

    # Выводим список всех пользователей
    users_text.insert(tk.END, "ID\tИмя\n")
    for user in user_list:
        users_text.insert(tk.END, f"{user.get_user_id()}\t{user.get_name()}\n")

    # Метка и поле ввода для добавления нового пользователя
    tk.Label(manage_window, text="Новый пользователь").pack(pady=10)
    new_user_frame = tk.Frame(manage_window)
    new_user_frame.pack()

    tk.Label(new_user_frame, text="ID Пользователя:").grid(row=0, column=0, padx=5, pady=5)
    entry_new_user_id = tk.Entry(new_user_frame)
    entry_new_user_id.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(new_user_frame, text="Имя пользователя:").grid(row=1, column=0, padx=5, pady=5)
    entry_new_user_name = tk.Entry(new_user_frame)
    entry_new_user_name.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(new_user_frame, text="Пароль пользователя:").grid(row=2, column=0, padx=5, pady=5)
    entry_new_user_password = tk.Entry(new_user_frame, show="*")
    entry_new_user_password.grid(row=2, column=1, padx=5, pady=5)

    def add_new_user():
        new_user_id = entry_new_user_id.get()
        new_user_name = entry_new_user_name.get()
        new_user_password = entry_new_user_password.get()

        if not new_user_id.isdigit():
            messagebox.showerror("Ошибка", "Идентификатор пользователя должен быть числом.")
            return

        new_user_id = int(new_user_id)
        new_user = User(new_user_id, new_user_name, new_user_password)
        admin.add_user(user_list, new_user)

        # Обновляем список пользователей в текстовом поле
        users_text.delete(1.0, tk.END)
        users_text.insert(tk.END, "ID\tИмя\n")
        for user in user_list:
            users_text.insert(tk.END, f"{user.get_user_id()}\t{user.get_name()}\n")

        messagebox.showinfo("Выполнено", "Пользователь успешно добавлен")

    add_user_button = tk.Button(new_user_frame, text="Добавить пользователя", command=add_new_user)
    add_user_button.grid(row=3, columnspan=2, pady=10)

    # Кнопка для удаления пользователя
    def remove_user():
        user_id_to_remove = entry_remove_user_id.get()

        if not user_id_to_remove.isdigit():
            messagebox.showerror("Ошибка", "Идентификатор пользователя должен быть числом.")
            return

        user_id_to_remove = int(user_id_to_remove)
        admin.remove_user(user_list, user_id_to_remove)

        # Обновляем список пользователей в текстовом поле
        users_text.delete(1.0, tk.END)
        users_text.insert(tk.END, "ID\tИмя\n")
        for user in user_list:
            users_text.insert(tk.END, f"{user.get_user_id()}\t{user.get_name()}\n")

        messagebox.showinfo("Выполнено", "Пользователь успешно удален")

    tk.Label(manage_window, text="Удалить пользователя").pack(pady=10)
    remove_user_frame = tk.Frame(manage_window)
    remove_user_frame.pack()

    tk.Label(remove_user_frame, text="ID Пользователя:").grid(row=0, column=0, padx=5, pady=5)
    entry_remove_user_id = tk.Entry(remove_user_frame)
    entry_remove_user_id.grid(row=0, column=1, padx=5, pady=5)

    remove_user_button = tk.Button(remove_user_frame, text="Удалить пользователя", command=remove_user)
    remove_user_button.grid(row=1, columnspan=2, pady=10)

# Функция для проверки данных пользователя
def login():
    user_id = entry_user_id.get()
    password = entry_password.get()

    if not user_id.isdigit():
        messagebox.showerror("Ошибка авторизации", "Идентификатор пользователя должен быть числом.")
        return

    user_id = int(user_id)

    for user in user_list:
        if user.get_user_id() == user_id and user.check_password(password):
            show_welcome_window(user.get_name(), user.get_access_level())
            return

    messagebox.showerror("Ошибка авторизации", "Неверный идентификатор пользователя или пароль")

# Создаем окно приложения
app = tk.Tk()
app.title("Вход пользователя")
app.geometry("300x130")  # Устанавливаем начальный размер окна
app.resizable(True, True)  # Разрешаем изменение размеров окна

# Метка и поле ввода для ID пользователя
tk.Label(app, text="ID Пользователя:").grid(row=0, column=0)
entry_user_id = tk.Entry(app)
entry_user_id.grid(row=0, column=1)

# Метка и поле ввода для пароля
tk.Label(app, text="Пароль:").grid(row=1, column=0)
entry_password = tk.Entry(app, show="*")
entry_password.grid(row=1, column=1)

# Кнопка для входа
login_button = tk.Button(app, text="Вход", command=login)
login_button.grid(row=2, columnspan=2, pady=10)

# Запускаем основной цикл обработки событий
app.mainloop()