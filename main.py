from tkinter import *
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('phonebook.db')
c = conn.cursor()
c.execute("PRAGMA table_info(contacts)")
print(c.fetchall())
c.execute('''CREATE TABLE IF NOT EXISTS contacts
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name text, surname text, phone text, email text)''')
conn.commit()

# Функиция обработки ошибок
def handle_error(error):
    root = Tk()
    root.withdraw()  # Скрываем главное окно
    error_window = Toplevel(root)
    error_window.title("Ошибка")
    error_window.geometry("300x200")

    label = Label(error_window, text=error, wraplength=280, justify="left", font=("Arial", 10))
    label.pack(pady=20)

    button = Button(error_window, text="OK", command=error_window.destroy)
    button.pack()

# Функция добавить контакт
def add_contact():
    try:
        name = e_name.get()
        surname = c_surname.get()
        phone = e_telephone.get()
        email = e_email.get()

        c.execute("INSERT INTO contacts (name, surname, phone, email) VALUES (?, ?, ?, ?)",
                  (name, surname, phone, email))
        conn.commit()
        update_tree()
    except sqlite3.Error as e:
        handle_error(f"Ошибка при добавлении контакта: {e}")
    
# Функция удаления контакта
def delete_contact():
    try:
        selected_item = tree.selection()[0]
        values = tree.item(selected_item)['values']
        c.execute("DELETE FROM contacts WHERE id=?", 
              (values[0],))
        conn.commit()
        update_tree()
    except sqlite3.Error as e:
        handle_error(f"Ошибка удаления контакта : {e}")

# Обновление контакта
def update_contact():
    try:
        selected_item = tree.selection()[0]
        values = tree.item(selected_item)['values']
        new_name = e_name.get()
        new_surname = c_surname.get()
        new_phone = e_telephone.get()
        new_email = e_email.get()

        c.execute("UPDATE contacts SET name=?, surname=?, phone=?, email=? WHERE id=?", 
              (new_name, new_surname, new_phone, new_email, values[0]))
        conn.commit()
        update_tree()
    except sqlite3.Error as e:
        handle_error(f"Ошибка при изменении контакта контакта: {e}")

# Обновление дерева контактов
def update_tree():
    for item in tree.get_children():
        tree.delete(item)
    
    c.execute("SELECT * FROM contacts")
    rows = c.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)

# Функция отображения контактов
def show_contacts():
    update_tree()

# Цвета 
co0 = "#ffffff"
co1 = "#DABFFF"
co2 = "#907AD6"

window = Tk()
window.title("PhoneBook")
window.geometry('485x450')
window.configure(background=co0)
window.resizable(width=FALSE, height=FALSE)

# Рамки
frame_up = Frame(window, width=500, height=50, bg=co2)
frame_up.grid(row=0, column=0, padx=0, pady=1)

frame_down = Frame(window, width=500, height=150, bg=co0)
frame_down.grid(row=1, column=0, padx=0, pady=1)

frame_table = Frame(window, width=500, height=100, bg=co0, relief="flat")
frame_table.grid(row=2, column=0, columnspan=2, padx=10, pady=1, sticky=NW)

# Табличка
def show():
    global tree

    listheader = ['ID', 'Имя', 'Фамилия', 'Номер', 'Email']

    demo_list = []

    c.execute("SELECT * FROM contacts")
    rows = c.fetchall()

    for row in rows:
        demo_list.append(row)

    tree = ttk.Treeview(frame_table, selectmode="extended", columns=listheader, show="headings")

    vsb = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_table, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    # tree head
    tree.heading(0, text='ID', anchor=NW)
    tree.heading(1, text='Имя', anchor=NW)
    tree.heading(2, text='Фамилия', anchor=NW)
    tree.heading(3, text='Номер', anchor=NW)
    tree.heading(4, text='Email', anchor=NW)

    # tree columns
    tree.column(0, width=60, anchor='center')
    tree.column(1, width=110, anchor='nw')
    tree.column(2, width=110, anchor='nw')
    tree.column(3, width=110, anchor='nw')
    tree.column(4, width=110, anchor='nw')

    for item in demo_list:
        tree.insert('', 'end', values=item)

show()  # Вызов функции show()

# Виджеты Frame_up
app_name = Label(frame_up, text="PhoneBook", height=1, font=('Verdana 17 bold'), bg=co2, fg=co0)
app_name.place(x=5, y=5)

# Виджеты frame_down
l_name = Label(frame_down, text="Имя :", width=20, height=1, font=('Ivy 10'), bg=co0, anchor=NW)
l_name.place(x=10, y=20)
e_name = Entry(frame_down, width=25, justify='left', highlightthickness=1, relief="solid")
e_name.place(x=80, y=20)

l_surname = Label(frame_down, text="Фамилия :", width=20, height=1, font=('Ivy 10'), bg=co0, anchor=NW)
l_surname.place(x=10, y=50)
c_surname = Entry(frame_down, width=25, justify='left', highlightthickness=1, relief="solid")
c_surname.place(x=80, y=50)

l_telephone = Label(frame_down, text="Номер :", height=1, font=('Ivy 10'), bg=co0, anchor=NW)
l_telephone.place(x=10, y=80)
e_telephone = Entry(frame_down, width=25, justify='left', highlightthickness=1, relief="solid")
e_telephone.place(x=80, y=80)

l_email = Label(frame_down, text="Email :", height=1, font=('Ivy 10'), bg=co0, anchor=NW)
l_email.place(x=10, y=110)
e_email = Entry(frame_down, width=25, justify='left', highlightthickness=1, relief="solid")
e_email.place(x=80, y=110)

b_search = Button(frame_down, text="Поиск", height=1, bg=co2, fg=co0, font=('Ivy 8 bold'))
b_search.place(x=280, y=20)
e_search = Entry(frame_down, width=16, justify='left', font=('Ivy 11'), highlightthickness=1, relief="solid")
e_search.place(x=337, y=20)

b_view = Button(frame_down, text="Список контактов", height=1, bg=co2, fg=co0, font=('Ivy 8 bold'), command=show_contacts)
b_view.place(x=280, y=50)

b_add = Button(frame_down, text="Добавить", width=10, height=1, bg=co2, fg=co0, font=('Ivy 8 bold'), command=add_contact)
b_add.place(x=400, y=50)

b_update = Button(frame_down, text="Обновить", width=10, height=1, bg=co2, fg=co0, font=('Ivy 8 bold'), command=update_contact)
b_update.place(x=400, y=80)

b_update = Button(frame_down, text="Удалить", width=10, height=1, bg=co2, fg=co0, font=('Ivy 8 bold'), command=delete_contact)
b_update.place(x=400, y=110)

mainloop()