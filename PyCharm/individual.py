#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import jsonschema
from jsonschema import validate
import argparse


def load_data():
    data = []
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            data = json.load(file)
            validate(data, schema)
    return data


def save_data(data):
    validate(data, schema)
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)


def exit_to_program():
    print('всего доброго')
    save_data(lst_planes)
    return exit(1)


def help_program():
    print("add - добавление рейса\n"
          "help - помощь по командам\n"
          "select \"пункт назначения\" - вывод самолетов летящих в п.н.\n"
          "display_plane - вывод всех самолетов\n"
          "exit - выход из программы")


def add_program(planes):
    plane = dict()
    plane["destination"] = input("Пункт назначения:\n")
    plane["flight_number"] = int(input("Номер рейса:\n"))
    plane["type_plane"] = input("Тип самолета\n")
    planes.append(plane)
    planes.sort(key=lambda key_plane: key_plane.get("flight_number"))
    return planes


def select_program(planes):
    lst = list(map(lambda x: x.get("destination"), planes))
    point = input('выберите нужное вам место\n')
    print("результаты поиска")
    if point in lst:
        print('рейсы в эту точку')
        for i in planes:
            if point == i["destination"]:
                print(f"{i['flight_number']}........{i['type_plane']}")
    else:
        print("рейсов не найдено")


def error():
    print('неверная комманда')


def display_plane(staff):
    if staff:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
                '-' * 4,
                '-' * 30,
                '-' * 20,
                '-' * 8
            )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "№",
                "Направление",
                "Тип самолета",
                "рейс"
            )
        )
        print(line)

        for idx, worker in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    worker.get('destination', ''),
                    worker.get('type_plane', ''),
                    worker.get('flight_number', 0)
                )
            )
            print(line)

    else:
        print("рейсов не найдено")


def menu(lst_plane):
    command = input('введите команду("help" - руководство по командам)\n>>>').lower()
    if command == 'exit':
        exit_to_program()
    elif command == 'help':
        help_program()
    elif command == 'add':
        lst_plane = add_program(lst_plane)
    elif command == 'select':
        select_program(lst_plane)
    elif command == 'display_plane':
        display_plane(lst_plane)
    else:
        error()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Программа управления рейсами самолетов')
    parser.add_argument('--file', help='Путь к файлу JSON для сохранения и чтения данных')
    args = parser.parse_args()

    data_file = args.file if args.file else input("введите расположение файла: ")

    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "flight_number": {"type": "integer"},
                "type_plane": {"type": "string"}
            },
            "required": ["destination", "flight_number", "type_plane"]
        }
    }

    lst_planes = load_data()

    while True:
        menu(lst_planes)
