import ntpath
import os
import os.path
import shutil
from tkinter import *
from tkinter import filedialog
import xlsxwriter
import json

def search_start():

    if new_files_folder_path.get() == 'Папка не выбрана':
        lbl_button_start_text.set("Поиск не выполнен! Выберите папку с новыми файлами!")
        return

    if old_files_folder_path.get() == 'Папка не выбрана':
        lbl_button_start_text.set("Поиск не выполнен! Выберите папку со старыми файлами!")
        return

    if report_files_folder_path.get() == 'Папка не выбрана':
        lbl_button_start_text.set("Поиск не выполнен! Выберите папку для результатов поиска!")
        return


    if not (os.path.exists(new_files_folder_path.get())):
        lbl_button_start_text.set("Замена не выполнена! Папка новых файлов не существует!")
        return

    if not (os.path.exists(old_files_folder_path.get())):
        lbl_button_start_text.set("Замена не выполнена! Папка старых файлов не существует!")
        return

    if not (os.path.exists(report_files_folder_path.get())):
        lbl_button_start_text.set("Замена не выполнена! Папка для результатов поиска не существует!")
        return
    

    if os.listdir(report_files_folder_path.get()):
        lbl_button_start_text.set("Поиск не выполнен! Нужно очистить папку для результатов поиска!")
        return

    if not (os.listdir(new_files_folder_path.get())):
        lbl_button_start_text.set("Поиск не выполнен! Папка с новыми файлами пуста!")
        return

    if not (os.listdir(old_files_folder_path.get())):
        lbl_button_start_text.set("Поиск не выполнен! Папка со старыми файлами пуста!")
        return

    lbl_button_start_text.set("Выполняется поиск клонов . . .")
    window.update()

    def GetBytes(file_fullname):
        f = open(file_fullname, 'rb')
        return f.read()

    def GetFileList(folder):
        FileList = []
        for d, dirs, files in os.walk(folder):
            for f in files:
                FileList.append(d + "\\" + f)
        return FileList

    def ToFindClonesOfTheFile(new_file_fullname):
        i = 0
        new_file_shortname = ntpath.basename(new_file_fullname)
        new_file_text = GetBytes(new_file_fullname)
        d = {new_file_text: [0, new_file_fullname]}
        for root, dirs, files in os.walk(old_files_folder_path.get(), topdown=False):
            for name in files:
                if name == new_file_shortname:
                    file_name = os.path.join(root, name)
                    new_file_fullname = new_file_fullname.replace('\\', '/')
                    file_name = file_name.replace('\\', '/')
                    if not (file_name == new_file_fullname):
                        file_text = GetBytes(file_name)
                        i = i + 1
                        j = 0
                        for key in d.keys():
                            if key == file_text:
                                d[key][0] = d[key][0] + 1
                                j = 1
                        if j == 0:
                            d[file_text] = [1, file_name]

        path = report_files_folder_path.get() + "\\" + new_file_shortname
        os.mkdir(path)

        book = xlsxwriter.Workbook(path + "\\" + new_file_shortname[0:-4] + ".xlsx")
        sheet = book.add_worksheet('Лист1')
        header = book.add_format({'bold': True, 'fg_color': '#D7E4BC', 'border': 1})
        center = book.add_format({'align': 'center'})
        sheet.write(0, 0, "Имя файла", header)
        sheet.write(0, 1, new_file_shortname)
        sheet.write(1, 0, "Видов клонов", header)
        sheet.write(1, 1, len(d.keys()) - 1, center)
        sheet.write(2, 0, "Клонов", header)
        sheet.write(2, 1, i - d[new_file_text][0], center)
        sheet.write(3, 0, "Копий", header)
        sheet.write(3, 1, d[new_file_text][0], center)
        sheet.write(4, 0, "Клонов и копий", header)
        sheet.write(4, 1, i, center)
        sheet.write(5, 0, "Исходный файл", header)
        sheet.write_url(5, 2, new_file_fullname)

        r_sheet.write(line, 0, new_file_shortname)
        r_sheet.write(line, 1, len(d.keys()) - 1, center_format)
        r_sheet.write(line, 2, i - d[new_file_text][0], center_format)
        r_sheet.write(line, 3, d[new_file_text][0], center_format)
        r_sheet.write(line, 4, i, center_format)

        shutil.copyfile(new_file_fullname, path + "\\" + new_file_shortname)

        if len(d.keys()) > 1:
            m = 0
            for k in d.keys():
                if k != new_file_text:
                    m = m + 1
                    shutil.copyfile(d[k][1],
                                    path + "\\Клон №" + str(m) + " - " + str(d[k][0]) + " шт. - " + new_file_shortname)
                    sheet.write(5 + m, 0, "Клон №" + str(m), header)
                    sheet.write(5 + m, 1, d[k][0], center)
                    sheet.write_url(5 + m, 2, d[k][1])

        sheet.set_column('A:A', 14)
        book.close()

    file_list = GetFileList(new_files_folder_path.get())

    if len(file_list) == 0:

        lbl_button_start_text.set("Поиск не выполнен! В папке с новыми файлами нет файлов для поиска!")


    else:

        r_book = xlsxwriter.Workbook(report_files_folder_path.get() + "\\Общий_отчёт.xlsx")

        r_sheet = r_book.add_worksheet('Лист1')

        header_format = r_book.add_format({'bold': True,
                                           'align': 'center',
                                           'valign': 'vcenter',
                                           'fg_color': '#D7E4BC',
                                           'border': 1})

        center_format = r_book.add_format({'align': 'center'})

        line = 0
        r_sheet.write(line, 0, "Файл", header_format)
        r_sheet.write(line, 1, "Видов клонов", header_format)
        r_sheet.write(line, 2, "Клонов", header_format)
        r_sheet.write(line, 3, "Копий", header_format)
        r_sheet.write(line, 4, "Клонов и копий", header_format)

        r_sheet.freeze_panes(1, 0)

        for newFile in file_list:
            line = line + 1
            ToFindClonesOfTheFile(newFile)

        r_sheet.write( line + 2, 0, "Поиск выполнен в папке " + old_files_folder_path.get())

        r_sheet.set_column('A:A', 40)
        r_sheet.set_column('B:B', 13)
        r_sheet.set_column('C:C', 8)
        r_sheet.set_column('D:D', 7)
        r_sheet.set_column('E:E', 14)

        r_book.close()

        lbl_button_start_text.set("Поиск клонов успешно выполнен! Отчет в папке для результатов поиска.")

window = Tk()
window.geometry('950x160')
window.resizable(width=False, height=False)
window.title("Поиск клонов файлов")

config = {"new_files_folder_path": 'Папка не выбрана', "old_files_folder_path": 'Папка не выбрана', "report_files_folder_path": 'Папка не выбрана'}

def on_exit():
    config["new_files_folder_path"] = new_files_folder_path.get()
    config["old_files_folder_path"] = old_files_folder_path.get()
    config["report_files_folder_path"] = report_files_folder_path.get()
    with open('ConfCloneSearch.json', 'w') as f:
        json.dump(config, f)
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_exit)

global new_files_folder_path
new_files_folder_path = StringVar()
global old_files_folder_path
old_files_folder_path = StringVar()
global report_files_folder_path
report_files_folder_path = StringVar()
global lbl_button_start_text
lbl_button_start_text = StringVar()
lbl_button_start_text.set("1) Выберите папки с файлами и для результатов поиска.\n2) Нажмите кнопку 'Начать поиск клонов'.")

if os.path.exists('ConfCloneSearch.json'):
    with open('ConfCloneSearch.json', 'r') as f:
        config = json.load(f)

new_files_folder_path.set(config["new_files_folder_path"])
old_files_folder_path.set(config["old_files_folder_path"])
report_files_folder_path.set(config["report_files_folder_path"])

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

def browse_button_report():
    filename = filedialog.askdirectory()
    if filename =='':
        return
    report_files_folder_path.set(filename)

button_new = Button(text="Выбрать папку с новыми файлами", command=browse_button_new, height=1, width=35)
button_new.grid(row=0, column=0)
lbl_new = Label(master=window, textvariable=new_files_folder_path)
lbl_new.grid(row=0, column=1, sticky=W)

button_old = Button(text="Выбрать папку со старыми файлами", command=browse_button_old, height=1, width=35)
button_old.grid(row=1, column=0)
lbl_old = Label(master=window, textvariable=old_files_folder_path)
lbl_old.grid(row=1, column=1, sticky=W)

button_report = Button(text="Выбрать папку для результатов поиска", command=browse_button_report, height=1, width=35)
button_report.grid(row=2, column=0)
lbl_report = Label(master=window, textvariable=report_files_folder_path)
lbl_report.grid(row=2, column=1, sticky=W)

button_start = Button(text="Начать поиск клонов", command=search_start, height=2, width=35)
button_start.grid(row=3, column=0)

lbl_button_start = Label(master=window, textvariable=lbl_button_start_text, font='Helvetica 10 bold', justify=LEFT)
lbl_button_start.grid(row=3, column=1, sticky=W)

window.mainloop()