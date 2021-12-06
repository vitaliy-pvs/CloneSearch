import os
import os.path
import shutil
from tkinter import *
from tkinter import filedialog
import json


def search_start():
    if result_folder_path.get() == 'Папка не выбрана':
        lbl_button_start_text.set("Поиск не выполнен! Выберите папку куда копировать!")
        return

    if not (os.path.exists(result_folder_path.get())):
        lbl_button_start_text.set("Поиск не выполнен! Папка куда копировать не существует!")
        return

    if os.listdir(result_folder_path.get()):
        lbl_button_start_text.set("Поиск не выполнен! Очистите папку куда копировать!")
        return

    if search_folder_path.get() == 'Папка не выбрана':
        lbl_button_start_text.set("Поиск не выполнен! Выберите папку где искать!")
        return

    if not (os.path.exists(search_folder_path.get())):
        lbl_button_start_text.set("Поиск не выполнен! Папка где искать не существует!")
        return

    if not (os.listdir(search_folder_path.get())):
        lbl_button_start_text.set("Поиск не выполнен! Папка где искать пуста!")
        return

    lbl_button_start_text.set("Выполняется поиск файлов . . .")
    window.update()

    file_name_string = result_text.get(1.0, END)
    file_name_list = file_name_string.split("\n")
    for name in file_name_list:
        if name == '':
            file_name_list.remove(name)

    if len(file_name_list) == 0:
        lbl_button_start_text.set("Поиск не выполнен! Список файлов для поиска пуст!")
    else:
        result_text.delete(1.0, END)
        window.update()
        res = "НАЙДЕНЫ:\n\n"
        for root, dirs, files in os.walk(search_folder_path.get(), topdown=False):
            if len(file_name_list) == 0:
                break
            for name in files:
                if len(file_name_list) == 0:
                    break
                if name[-3:] != 'PDF' and name[-3:] != 'pdf':
                    continue
                for file_name in file_name_list:
                    if name[:len(file_name)] == file_name:
                        old_full_file_name = os.path.join(root, name)
                        old_full_file_name = old_full_file_name.replace('\\', '/')
                        new_full_file_name = os.path.join(result_folder_path.get(), name)
                        new_full_file_name = new_full_file_name.replace('\\', '/')
                        shutil.copyfile(old_full_file_name, new_full_file_name)
                        res = res + file_name + ":\n" + name + "\n\n"
                        file_name_list.remove(file_name)
                        if len(file_name_list) == 0:
                            break
                        continue

        if len(file_name_list) != 0:
            res = res + "\nНЕ НАЙДЕНЫ:\n"
            for file_name in file_name_list:
                res = res + file_name + "\n"
        result_text.insert(1.0, res)
        lbl_button_start_text.set("Поиск файлов выполнен!")


window = Tk()
window.geometry('950x585')
window.resizable(width=False, height=False)
window.title("Поиск и копирование файлов формата PDF")

config = {"result_folder_path": 'Папка не выбрана', "search_folder_path": 'Папка не выбрана'}


def on_exit():
    config["result_folder_path"] = result_folder_path.get()
    config["search_folder_path"] = search_folder_path.get()
    with open('FileCopy.json', 'w') as file:
        json.dump(config, file)
    window.destroy()


window.protocol("WM_DELETE_WINDOW", on_exit)

global result_folder_path
result_folder_path = StringVar()
global search_folder_path
search_folder_path = StringVar()
global lbl_button_start_text
lbl_button_start_text = StringVar()
lbl_button_start_text.set(
    "1) Выберите папки где искать и куда копировать файлы.\n2) Нажмите кнопку 'Начать поиск файлов'.")

if os.path.exists('FileCopy.json'):
    with open('FileCopy.json', 'r') as f:
        config = json.load(f)

result_folder_path.set(config["result_folder_path"])
search_folder_path.set(config["search_folder_path"])


def browse_button_result():
    filename = filedialog.askdirectory()
    if filename == '':
        return
    result_folder_path.set(filename)


def browse_button_search():
    filename = filedialog.askdirectory()
    if filename == '':
        return
    search_folder_path.set(filename)


def paste():
    result_text.delete(1.0, END)
    try:
        clipboard = window.clipboard_get()
        result_text.insert("insert", clipboard)
    except TclError:
        result_text.insert("insert", 'Скопируйте текст в буфер обмена и еще раз нажмите кнопку!')


button_copy = Button(text="Выбрать папку куда копировать", command=browse_button_result, height=1, width=35)
button_copy.grid(row=0, column=0)
lbl_copy = Label(master=window, textvariable=result_folder_path)
lbl_copy.grid(row=0, column=1, sticky=W)

button_search = Button(text="Выбрать папку где искать", command=browse_button_search, height=1, width=35)
button_search.grid(row=1, column=0)
lbl_search = Label(master=window, textvariable=search_folder_path)
lbl_search.grid(row=1, column=1, sticky=W)

button_start = Button(text="Начать поиск файлов", command=search_start, height=2, width=35)
button_start.grid(row=2, column=0)

lbl_button_start = Label(master=window, textvariable=lbl_button_start_text, font='Helvetica 10 bold', justify=LEFT)
lbl_button_start.grid(row=2, column=1, sticky=W)

lbl_result_text = Label(master=window, text="Скопируйте имена файлов\nв формате PDF\nв буфер обмена и вставьте\n" +
                                            "нажатием кнопки внизу.\nИли просто наберите имена\nфайлов с клавиатуры в\nтекстовое поле справа." +
                                            "\n\nКаждое имя файла должно\nначинаться с новой строки\n" +
                                            "и не иметь расширения.\n\n" +
                                            "После выполнения поиска\nздесь появятся результаты.")
lbl_result_text.grid(row=3, column=0, sticky=W)

result_text = Text(width=65, height=20, bg="white", wrap=WORD)
result_text.grid(row=3, column=1, sticky=W)

button_paste = Button(text="Вставить текст из буфера", command=paste, height=2, width=35)
button_paste.grid(row=4, column=1)

window.mainloop()
