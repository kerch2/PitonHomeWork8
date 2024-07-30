"""
Задача. Решение в группах Создать телефонный справочник с
возможностью импорта и экспорта данных в формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в текстовом файле
3. Пользователь может ввести одну из характеристик для поиска определенной
записи(Например имя или фамилию человека)
4. Использование функций. Ваша программа не должна быть линейной

Задание:
В телефонной книге необходимо дополнить код функцией, которая записывает содержимое строки,
с указанным номером, в другой файл.


"""

from csv import DictReader, DictWriter
from os.path import exists


class Name_error(Exception):
    def __init__(self, txt):
        self.txt = txt


def getdata():
    flag = False
    while not flag:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise Name_error("Слишком короткое имя")
            last_name = input("Введите фамилию: ")
            if len(last_name) < 3:
                raise Name_error("Слишком короткое имя")
            phone = input("Введите номер телефона в полном формате: ")
            if not check_phone(phone):
                raise Name_error("Некорректный номер телефона")
        except Name_error as err:
            print(err)
        else:
            flag = True

    return ([first_name, last_name, phone])


def check_phone(phone):  # проверка на префикс и цифры в номере телефона
    if phone[0] != '+':
        print("Вы не ввели префикс")
        return False
    for el in phone[1:]:
        if not el.isdigit():
            print("Ошибка ввода цифр")
            return False
    return True


def create_file(filename):
    with open(filename, 'w', encoding='UTF-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()


def read_file(filename):
    with open(filename, 'r', encoding='UTF-8') as data:
        f_r = DictReader(data)
        return list(f_r)


def write_file(filename, lst):
    res = read_file(filename)
    obj = {'Имя': lst[0], 'Фамилия': lst[1], 'Телефон': lst[2]}
    res.append((obj))
    standart_write(filename, res)


def row_search(filename):
    last_name = input("Введите фамилию :")
    res = read_file(filename)
    for row in res:
        if last_name == row['Фамилия']:
            #            print(row)
            return row
    return print("Запись не найдена")


def delete_row(filename):
    row_number = int(input("Введите номер строки  :"))
    res = read_file(filename)
    res.pop(row_number - 1)
    standart_write(filename, res)


def standart_write(filename, res):
    with open(filename, 'w', encoding='UTF-8') as data:
        f_w = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_w.writeheader()
        f_w.writerows(res)


def change_row(filename):
    row_number = int(input("Введите номер строки  :"))
    res = read_file(filename)
    data = getdata()
    res[row_number - 1]["Имя"] = data[0]
    res[row_number - 1]["Фамилия"] = data[1]
    res[row_number - 1]["Телефон"] = data[2]
    standart_write(filename, res)


def copy_row_to_file(filename, file_copy):
    row_number = int(input("Введите номер строки  :"))
    res = read_file(filename)
    our_str = res[row_number - 1]
#    print(our_str)
    res = read_file(file_copy)
    res.append(our_str)
    standart_write(file_copy, res)
    print(f'строка {row_number} скопирована в файл')


filename = 'phone.csv'
file_copy = 'copy_phone.csv'


def main():
    while True:
        command = input("Введите команду:  ")
        if command == "q":  # Выход из программы
            break
        elif command == "w":  # Создать файл
            if not exists(filename):
                create_file(filename)
            write_file(filename, getdata())
        elif command == "r":  # Прочитать файл
            if not exists(filename):
                print("Файл не существует, создайте его")
                continue
            print(read_file(filename))
        elif command == "f":  # Поиск строки
            if not exists(filename):
                print("Файл не существует, создайте его")
                continue
            print(row_search(filename))
        elif command == "d":  # Удаление строки
            if not exists(filename):
                print("Файл не существует, создайте его")
                continue
            delete_row(filename)
        elif command == "c":  # Изменение строки
            if not exists(filename):
                print("Файл не существует, создайте его")
                continue
            change_row(filename)
        elif command == "cc":  # Копирование строки в другой файл
            if not exists(filename):
                print("Файл не существует, создайте его")
                continue
            if not exists(file_copy):
                create_file(file_copy)
            copy_row_to_file(filename, file_copy)


main()

