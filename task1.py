from tkinter import *
from tkinter import ttk, scrolledtext
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
from tkinter import messagebox
import psutil
from os import remove
import json
import xml.etree.ElementTree as ET
import os
import zipfile

root = Tk()

root.title("Практика 1. Руденок М.И, БСБО-02-20")
root.resizable(False, False)

WIDTH, HEIGHT = 900, 700

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (WIDTH / 2)
y = (screen_height / 2) - (HEIGHT / 2)

root.geometry(F"{WIDTH}x{HEIGHT}+{int(x)}+{int(y) - 40}")

tab_panel = ttk.Notebook(root, padding=5)

tab1 = Frame(tab_panel)
tab2 = Frame(tab_panel)
tab3 = Frame(tab_panel)
tab4 = Frame(tab_panel)
tab5 = Frame(tab_panel)

tab_panel.add(tab1, text="Информация о дисках")
tab_panel.add(tab2, text="Работа с файлами")
tab_panel.add(tab3, text="Работа с JSON")
tab_panel.add(tab4, text="Работа с XML")
tab_panel.add(tab5, text="Работа с ZIP")

tab_panel.pack(expand=True, fill=BOTH)

############################################################################################### Информация о дисках

info_view = scrolledtext.ScrolledText(tab1, padx=5, pady=3, font="Consolas 11", height=33, width=107)
info_view.place(x=3, y=10)

def show_fs_info():

    def write(text: str) -> None:
        info_view["state"] = "normal"
        info_view.delete(1.0, END)
        info_view.insert(1.0, text)

    def get_drive_info(drive):
        drive_info = {}
        drive_info["Название"] = drive.device
        drive_info["Тип"] = drive.fstype
        
        if psutil.disk_usage(drive.mountpoint).total:
            drive_info["Объём диска"] = psutil.disk_usage(drive.mountpoint).total
            drive_info["Свободное пространство"] = psutil.disk_usage(drive.mountpoint).free
            drive_info["Метка"] = drive.mountpoint
        return drive_info

    drives = psutil.disk_partitions()
    final_string = ""
    for drive in drives:
        drive_info = get_drive_info(drive)
        final_string += f"\n\nНазвание: {drive_info['Название']}\nТип: {drive_info['Тип']}"

        if "Объём диска" in drive_info:
            final_string += f'\nОбъём диска: {drive_info["Объём диска"]}\nСвободное пространство: {drive_info["Свободное пространство"]}\nМетка: {drive_info["Метка"]}'

    write(final_string.strip())
    info_view["state"] = "disabled"

bColor = "#CBCBCB"
bTextColor = fg="#000000"
bFont = "Calibri 11 bold"

refresh_button = Button(tab1, text="Обновить данные", width=25, height=2, bg=bColor, font=bFont, fg=bTextColor, command=show_fs_info, bd=0,)
refresh_button.place(x=666, y=616)

############################################################################################### Работа с файлами

text_view = scrolledtext.ScrolledText(tab2, padx=5, pady=3, font="Consolas 11", height=32, width=107, state="disabled")
text_view.place(x=3, y=28)

current_file = ""

label = Label(tab2, font="Calibri 11", text="Файл не выбран")
label.place(x=0, y=3)

def open_file():
    global current_file
    file = askopenfilename(title="Открытие файла", filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
    if file == "": return
    text_view["state"] = "normal"
    bSaveTxt["state"] = "normal"
    current_file = file
    label["text"] = os.path.basename(file)
    text_view.delete(1.0, END)
    with open(file, "r", encoding="utf-8") as f:
        text_view.insert(1.0, f.read())

def save_file():
    if current_file == "": return
    text = text_view.get(1.0, END).rstrip()
    with open(current_file, "w", encoding="utf-8") as f:
        f.write(text)

def delete_txt():
    file = askopenfilename(title="Удаление файла", filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
    if file == "": return

    choice = messagebox.askyesno("Удаление", f"Вы действительно хотите удалить файл {os.path.basename(file)}? Отменить данное действие будет невозможно.")
    if not choice: return

    if file == current_file:
        label["text"] += " (удалён)"
        bSaveTxt["state"] = "disabled"
        text_view["state"] = "disabled"
    remove(file)

def create_file():
    path = asksaveasfilename(title="Создание файла", filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")], defaultextension=".txt")
    if path == "": return
    with open(path, "w", encoding="utf-8"): pass

bSaveTxt = Button(tab2, text="Сохранить изменения", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=save_file, bd=0, state="disabled")
bCreateTxt = Button(tab2, text="Создать файл", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=create_file, bd=0)
bOpenTxt = Button(tab2, text="Открыть файл", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=open_file, bd=0)
bDeleteTxt = Button(tab2, text="Удалить файл", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=delete_txt, bd=0)

bSaveTxt.place(x=3, y=616)
bCreateTxt.place(x=358, y=616)
bOpenTxt.place(x=532, y=616)
bDeleteTxt.place(x=706, y=616)

############################################################################################### Работа с JSON

lFio = Label(tab3, text="ФИО", font="Calibri 11")
lNumber = Label(tab3, text="Номер телефона", font="Calibri 11")
lAddress = Label(tab3, text="Адрес", font="Calibri 11")

lFio.place(x=0, y=3)
lNumber.place(x=0, y=45)
lAddress.place(x=0, y=87)

eFio = Entry(tab3, font="Calibri 11", bd=2)
eNumber = Entry(tab3, font="Calibri 11", bd=2)
eAddress = Entry(tab3, font="Calibri 11", bd=2)

eFio.place(x=4, y=25, width=285)
eNumber.place(x=4, y=67, width=285)
eAddress.place(x=4, y=109, width=285)

json_view = scrolledtext.ScrolledText(tab3, padx=5, pady=3, font="Consolas 11", height=26, width=107, state="disabled")
json_view.place(x=3, y=194)

json_list = []

def get_formatted_data(data_list: list) -> str:
    result = ""
    for d in data_list:
        result += f"\nФИО: {d['name']}\nТелефон: {d['number']}\nАдрес: {d['address']}\n"
    return result.strip()

def add_json():
    global json_list
    json_view["state"] = "normal"
    json_view.delete(1.0, END)
    fio, number, address = eFio.get(), eNumber.get(), eAddress.get()
    
    if fio.strip() == "": fio = "None"
    if number.strip() == "": number = "None"
    if address.strip() == "": address = "None"

    json_list.append({"name":fio, "number":number, "address":address})
    json_view.insert(1.0, get_formatted_data(json_list))

    bSaveJson["state"] = "normal"
    json_view["state"] = "disabled"

def read_json():
    global json_list
    file = askopenfilename(title="Открытие файла", filetypes=[("Файлы JSON", "*.json"), ("Все файлы", "*.*")])
    if file == "": return
    result = ""
    with open(file, "r", encoding="utf-8") as f:
        json_data = json.loads(f.read())

    json_list = json_data["people"]
    for person in json_data["people"]:
       result += f"\nФИО: {person['name']}\nТелефон: {person['number']}\nАдрес: {person['address']}\n"

    json_view["state"] = "normal"
    json_view.delete(1.0, END)
    json_view.insert(1.0, result.strip())
    bSaveJson["state"] = "normal"
    json_view["state"] = "disabled"

def save_json():
    path = asksaveasfilename(title="Сохранение файла", filetypes=[("Файлы JSON", "*.json"), ("Все файлы", "*.*")], defaultextension=".json")
    if path == "": return
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"people":json_list}, f, indent=3, ensure_ascii=False)

def delete_file():
    file = askopenfilename(title="Удаление файла", filetypes=[("Все файлы", "*.*")])
    if file == "": return

    choice = messagebox.askyesno("Удаление", f"Вы действительно хотите удалить файл {os.path.basename(file)}? Отменить данное действие будет невозможно.")
    if not choice: return
    
    remove(file)

bAddJson = Button(tab3, text="Добавить запись", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=add_json, bd=0)
bReadJson = Button(tab3, text="Прочитать файл", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=read_json, bd=0)
bSaveJson = Button(tab3, text="Сохранить файл", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=save_json, bd=0, state="disabled")
bDeleteJson = Button(tab3, text="Удалить файл", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=delete_file, bd=0)

bAddJson.place(x=4, y=140)
bReadJson.place(x=358, y=140)
bSaveJson.place(x=532, y=140)
bDeleteJson.place(x=706, y=140)

############################################################################################### Работа с XML

lFio2 = Label(tab4, text="ФИО", font="Calibri 11")
lNumber2 = Label(tab4, text="Номер телефона", font="Calibri 11")
lAddress2 = Label(tab4, text="Адрес", font="Calibri 11")

lFio2.place(x=0, y=3)
lNumber2.place(x=0, y=45)
lAddress2.place(x=0, y=87)

eFio2 = Entry(tab4, font="Calibri 11", bd=2)
eNumber2 = Entry(tab4, font="Calibri 11", bd=2)
eAddress2 = Entry(tab4, font="Calibri 11", bd=2)

eFio2.place(x=4, y=25, width=285)
eNumber2.place(x=4, y=67, width=285)
eAddress2.place(x=4, y=109, width=285)

xml_view = scrolledtext.ScrolledText(tab4, padx=5, pady=3, font="Consolas 11", height=26, width=107, state="disabled")
xml_view.place(x=3, y=194)

people_data = []

def add_xml():
    fio, number, address = eFio2.get(), eNumber2.get(), eAddress2.get()

    if fio.strip() == "": fio = "None"
    if number.strip() == "": number = "None"
    if address.strip() == "": address = "None"

    people_data.append({"name": fio, "number": number, "address": address})

    xml_view["state"] = "normal"
    xml_view.insert(END, f"ФИО: {fio}\nТелефон: {number}\nАдрес: {address}\n\n")
    bSaveXml["state"] = "normal"
    xml_view["state"] = "disabled"

def read_xml():
    file = askopenfilename(title="Открытие файла", filetypes=[("Файлы XML", "*.xml"), ("Все файлы", "*.*")])
    if file == "": return

    tree = ET.parse(file).getroot()
    
    xml_view["state"] = "normal"

    xml_view.delete(1.0, END)
    people_data.clear()
    for child in tree:
            xml_view.insert(END, f"ФИО: {child[0].text}\nТелефон: {child[1].text}\nАдрес: {child[2].text}\n\n")
            people_data.append({"name": child[0].text, "number": child[1].text, "address": child[2].text})


    xml_view["state"] = "disabled"

def save_xml():
    path = asksaveasfilename(title="Сохранение файла", filetypes=[("Файлы XML", "*.xml"), ("Все файлы", "*.*")], defaultextension=".xml")
    if path == "": return

    xml_doc = ET.Element("people")

    for pers in people_data:
        person = ET.SubElement(xml_doc, "person")
        ET.SubElement(person, "name").text = pers['name']
        ET.SubElement(person, "number").text = pers['number']
        ET.SubElement(person, "address").text = pers['address']
        
    tree = ET.ElementTree(xml_doc)
    ET.indent(tree, space="\t")
    tree.write(path, encoding="UTF-8", xml_declaration=True)


bAddXml = Button(tab4, text="Добавить запись", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=add_xml,
              bd=0)
bReadXml = Button(tab4, text="Прочитать файл", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=read_xml,
               bd=0)
bSaveXml = Button(tab4, text="Сохранить файл", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=save_xml,
               bd=0, state="disabled")
bDeleteXml = Button(tab4, text="Удалить файл", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor,
                     command=delete_file, bd=0)

bAddXml.place(x=4, y=140)
bReadXml.place(x=358, y=140)
bSaveXml.place(x=532, y=140)
bDeleteXml.place(x=706, y=140)

############################################################################################### Работа с ZIP

zip_view = scrolledtext.ScrolledText(tab5, padx=5, pady=3, font="Consolas 11", height=33, width=107, state="disabled")
zip_view.place(x=3, y=10)

is_open = False
current_zip = None
added_files = []

def save_zip():
    global added_files
    path = asksaveasfilename(title="Сохранение архива", filetypes=[("Файлы ZIP", "*.zip"), ("Все файлы", "*.*")], defaultextension=".zip")
    if path == "": return

    with zipfile.ZipFile(path, 'w') as zip_file:

        for file_path in added_files:
            file_name = os.path.basename(file_path)
            zip_file.write(file_path, file_name)

def add_zip():
    global added_files
    global is_open
    path = askopenfilename(title="Открытие файла", filetypes=[("Все файлы", "*.*")])
    if path == "": return

    file_name = os.path.basename(path)

    zip_view["state"] = "normal"

    if is_open:
        zip_view.delete(1.0, END)
        is_open = False

    zip_view.insert(END, f"Файл: {file_name}\nРазмер: {os.path.getsize(path) // 8} байт\n\n")
    added_files.append(path)

    bExtractZip["state"] = "disabled"
    bSaveZip["state"] = "normal"
    zip_view["state"] = "disabled"

def extract_zip():
    path = askdirectory(title="Выбор каталога для разархивирования")
    if path == "": return

    with zipfile.ZipFile(current_zip, 'r') as zip_file:
        zip_file.extractall(path)

def open_zip():
    global is_open
    global added_files
    global current_zip
    path = askopenfilename(title="Открытие архива", filetypes=[("Файлы ZIP", "*.zip"), ("Все файлы", "*.*")], defaultextension=".zip")
    if path == "": return

    current_zip = path
    is_open = True
    added_files.clear()

    zip_file = zipfile.ZipFile(path)
    file_count = len(zip_file.namelist())
    archive_size = os.path.getsize(path)

    info_string = "Архив: {}\n".format(os.path.basename(path))
    info_string += "Файлов в архиве: {}\n".format(file_count)
    info_string += "Размер архива: {} байт\n".format(archive_size)
    info_string += "-" * 107

    for file_info in zip_file.infolist():
        info_string += "\nФайл: {}\n".format(file_info.filename)
        info_string += "Размер: {} байт\n".format(file_info.file_size)

    zip_view["state"] = "normal"
    zip_view.delete(1.0, END)
    zip_view.insert(1.0, info_string)
    bExtractZip["state"] = "normal"
    bSaveZip["state"] = "disabled"
    zip_view["state"] = "disabled"

bSaveZip = Button(tab5, text="Сохранить архив", width=20, height=2, bg=bColor, font=bFont, fg=bTextColor, command=save_zip, bd=0, state="disabled")
bAddZip = Button(tab5, text="Добавить файл в архив", width=19, height=2, bg=bColor, font=bFont, fg=bTextColor, command=add_zip, bd=0)
bOpenZip = Button(tab5, text="Открыть архив", width=19, height=2, bg=bColor, font=bFont, fg=bTextColor, command=open_zip, bd=0)
bDeleteZip = Button(tab5, text="Удалить архив", width=19, height=2, bg=bColor, font=bFont, fg=bTextColor, command=delete_file, bd=0)
bExtractZip = Button(tab5, text="Разархивировать", width=19, height=2, bg=bColor, font=bFont, fg=bTextColor, command=extract_zip, bd=0, state="disabled")

bSaveZip.place(x=3, y=616)
bAddZip.place(x=222, y=616)
bOpenZip.place(x=386, y=616)
bExtractZip.place(x=550, y=616)
bDeleteZip.place(x=714, y=616)

if __name__ == "__main__":
    os.system("cls")
    show_fs_info()
    root.mainloop()