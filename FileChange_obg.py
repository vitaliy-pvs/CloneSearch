import ntpath
import os
import os.path
import shutil
from tkinter import *
from tkinter import filedialog
import json


class NewFile:

    def __init__(self, full_name):
        self.__full_name = full_name
        self.__short_name = ntpath.basename(full_name)
        self.__replacements_list = []
        self.__canceled_replacements_list = []

    def get_full_name(self):
        return self.__full_name
    def get_short_name(self):
        return self.__short_name
    def get_replacements(self):
        return len(self.__replacements_list)
    def get_canceled_replacements(self):
        return len(self.__canceled_replacements_list)
    def get_replacements_list(self):
        return self.__replacements_list
    def get_canceled_replacements_list(self):
        return self.__canceled_replacements_list

    def add_replacement(self, repl_file_name):
        self.__replacements_list.append(repl_file_name)
    def add_canceled_replacement(self, cancel_repl_file_name):
        self.__canceled_replacements_list.append(cancel_repl_file_name)


def search_start():



    if new_files_folder_path.get() == 'Папка не выбрана':
        lbl_button_start_text.set("Замена не выполнена! Выберите папку с новыми файлами!")
        return

    if not (os.path.exists(new_files_folder_path.get())):
        lbl_button_start_text.set("Замена не выполнена! Папка новых файлов не существует!")
        return

    if not (os.listdir(new_files_folder_path.get())):
        lbl_button_start_text.set("Замена не выполнена! Папка с новыми файлами пуста!")
        return





    if old_files_folder_path.get() == 'Папка не выбрана':
        lbl_button_start_text.set("Замена не выполнена! Выберите папку со старыми файлами!")
        return

    if not (os.path.exists(old_files_folder_path.get())):
        lbl_button_start_text.set("Замена не выполнена! Папка старых файлов не существует!")
        return

    if not (os.listdir(old_files_folder_path.get())):
        lbl_button_start_text.set("Замена не выполнена! Папка со старыми файлами пуста!")
        return

    lbl_button_start_text.set("Выполняется замена файлов . . .")
    window.update()

    def GetFileList(folder):
        FileList = []
        for d, dirs, files in os.walk(folder):
            for f in files:
                FileList.append(NewFile(d + "/" + f))
        return FileList

    def ToChangeFiles(file_list):
        for root, dirs, files in os.walk(old_files_folder_path.get(), topdown=False):
            for name in files:
                for new_file in file_list:
                    if name == new_file.get_short_name():
                        file_name = os.path.join(root, name)
                        file_name = file_name.replace('\\', '/')
                        if not (file_name == new_file.get_full_name()):
                            try:
                                os.remove(file_name)
                            except Exception:
                                new_file.add_canceled_replacement(file_name)
                                continue
                            else:
                                shutil.copyfile(new_file.get_full_name(), file_name)
                                new_file.add_replacement(file_name)
        return file_list

    file_list = GetFileList(new_files_folder_path.get())

    if len(file_list) == 0:

        lbl_button_start_text.set("Замена не выполнена! В папке с новыми файлами нет файлов для замены!")

    else:
        result_text.delete(1.0, END)
        window.update()
        res = ""
        j = 0
        zamen = 0
        otmen = 0

        file_list = ToChangeFiles(file_list)

        for newFile in file_list:
            j = j + 1
            res = res + "Файл №" + str(j) + ": '" + newFile.get_short_name() + "'\nЗамен: " + str(newFile.get_replacements()) + "\nОтмен: " + str(newFile.get_canceled_replacements()) + "\n"
            k = 1
            for i_url in newFile.get_canceled_replacements_list():
                res = res + "Отмена №" + str(k) + ": '" + i_url + "\n"
            res = res + "\n"
            zamen = zamen + newFile.get_replacements()
            otmen = otmen + newFile.get_canceled_replacements()

        lbl_button_start_text.set("Замена файлов выполнена! Замен: " + str(zamen) + "   Отмен: " + str(otmen))
        result_text.insert(1.0, res)


window = Tk()
window.geometry('950x535')
window.resizable(width=False, height=False)
window.title("Замена файлов")

config = {"new_files_folder_path": 'Папка не выбрана', "old_files_folder_path": 'Папка не выбрана'}

def on_exit():
    config["new_files_folder_path"] = new_files_folder_path.get()
    config["old_files_folder_path"] = old_files_folder_path.get()
    with open('FileChange_obg.json', 'w') as f:
        json.dump(config, f)
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_exit)

global new_files_folder_path
new_files_folder_path = StringVar()
global old_files_folder_path
old_files_folder_path = StringVar()
global lbl_button_start_text
lbl_button_start_text = StringVar()
lbl_button_start_text.set("1) Выберите папки с новыми и старыми файлами.\n2) Нажмите кнопку 'Начать замену файлов'.")

if os.path.exists('FileChange_obg.json'):
    with open('FileChange_obg.json', 'r') as f:
        config = json.load(f)

new_files_folder_path.set(config["new_files_folder_path"])
old_files_folder_path.set(config["old_files_folder_path"])

def browse_button_new():
    filename = filedialog.askdirectory()
    if filename =='':
        return
    new_files_folder_path.set(filename)

def browse_button_old():
    filename = filedialog.askdirectory()
    if filename =='':
        return
    old_files_folder_path.set(filename)

button_new = Button(text="Выбрать папку с новыми файлами", command=browse_button_new, height=1, width=35)
button_new.grid(row=0, column=0)
lbl_new = Label(master=window, textvariable=new_files_folder_path)
lbl_new.grid(row=0, column=1, sticky=W)

button_old = Button(text="Выбрать папку со старыми файлами", command=browse_button_old, height=1, width=35)
button_old.grid(row=1, column=0)
lbl_old = Label(master=window, textvariable=old_files_folder_path)
lbl_old.grid(row=1, column=1, sticky=W)

button_start = Button(text="Начать замену файлов", command=search_start, height=2, width=35)
button_start.grid(row=3, column=0)

lbl_button_start = Label(master=window, textvariable=lbl_button_start_text, font='Helvetica 10 bold', justify=LEFT)
lbl_button_start.grid(row=3, column=1, sticky=W)

lbl_result_text = Label(master=window, text="Результаты замены:")
lbl_result_text.grid(row=4, column=0, sticky=W)

result_text = Text(width=65, height=20, bg="white", wrap=WORD)
result_text.grid(row=4, column=1, sticky=W)

window.mainloop()