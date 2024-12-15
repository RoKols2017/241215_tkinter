import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def add_task():
    task = task_entry.get().strip()
    if task:
        tasks.append(task)
        update_list_box()
        task_entry.delete(0, tk.END)

def update_list_box():
    list_box.delete(0, tk.END)
    for i, task in enumerate(tasks):
        status = '✅' if task.startswith('✅') else ''
        list_box.insert(i, f"{status}{task}")

def mark_complete():
    selected_indices = list_box.curselection()
    for index in reversed(selected_indices):
        task = tasks[index]
        if not task.startswith('✅'):  # Проверяем, есть ли уже галочка
            tasks[index] = f"✅ {task}"  # Добавляем галочку только если её нет
    update_list_box()

def unmark_complete():
    selected_indices = list_box.curselection()
    for index in reversed(selected_indices):
        task = tasks[index]
        if task.startswith('✅'):
            tasks[index] = task.replace('✅ ', '')
    update_list_box()

def edit_task():
    selected_index = list_box.curselection()[0]
    task = tasks[selected_index]
    new_task = ask_string(f"Редактирование задачи:\n{task}", initialvalue=task)
    if new_task is not None:
        tasks[selected_index] = new_task.strip()
        update_list_box()

def ask_string(title, prompt="", initialvalue=""):
    top = tk.Toplevel(root)
    top.title(title)
    label = tk.Label(top, text=prompt)
    entry = tk.Entry(top)
    entry.insert(0, initialvalue)
    ok_button = tk.Button(top, text="OK", command=lambda: on_ok(top, entry))
    cancel_button = tk.Button(top, text="Отмена", command=top.destroy)

    label.pack(padx=5, pady=5)
    entry.pack(padx=5, pady=5)
    ok_button.pack(side=tk.RIGHT, padx=5, pady=5)
    cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)

    root.wait_window(top)
    return value

def on_ok(top, entry):
    global value
    value = entry.get()
    top.destroy()

def delete_task():
    selected_indices = list(list_box.curselection())
    selected_indices.sort(reverse=True)
    for index in selected_indices:
        del tasks[index]
    update_list_box()

def save_tasks():
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if filename:
        with open(filename, "w") as file:
            for task in tasks:
                file.write(f"{task}\n")
        messagebox.showinfo("Успех!", "Задачи сохранены!")

def load_tasks():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        try:
            with open(filename, "r") as file:
                global tasks
                tasks = [line.strip() for line in file.readlines()]
            update_list_box()
            messagebox.showinfo("Успех!", "Задачи загружены!")
        except Exception as e:
            messagebox.showerror("Ошибка!", f"Произошла ошибка при загрузке задач: {e}")

root = tk.Tk()
root.title("ToDo List App")
root.geometry("400x500")

tasks = []

# Поле ввода новой задачи
task_entry = tk.Entry(root)
task_entry.pack(fill=tk.X, padx=10, pady=(20,0))

# Кнопка добавления задачи
add_button = tk.Button(root, text="Добавить задачу", command=add_task)
add_button.pack(pady=(5,0))

# Список задач
list_box = tk.Listbox(root, height=15, selectmode=tk.EXTENDED)
list_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Кнопки управления задачами
button_frame = tk.Frame(root)
button_frame.pack(side=tk.LEFT, anchor='w', padx=10, pady=10)

complete_button = tk.Button(button_frame, text="Выполнено", command=mark_complete, bg="green", fg="white")
complete_button.grid(row=0, column=0, sticky='ew')

uncomplete_button = tk.Button(button_frame, text="Не выполнено", command=unmark_complete, bg="red", fg="white")
uncomplete_button.grid(row=0, column=1, sticky='ew')

edit_button = tk.Button(button_frame, text="Редактировать", command=edit_task)
edit_button.grid(row=2, column=0, sticky='ew')

delete_button = tk.Button(button_frame, text="Удалить", command=delete_task)
delete_button.grid(row=2, column=1, sticky='ew')

# Меню для сохранения/загрузки списка задач
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Сохранить", command=save_tasks)
file_menu.add_command(label="Загрузить", command=load_tasks)
menu_bar.add_cascade(label="Файл", menu=file_menu)
root.config(menu=menu_bar)

value = None

root.mainloop()