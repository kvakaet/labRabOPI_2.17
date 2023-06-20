#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import jsonschema
from jsonschema import validate
import click


@click.command()
@click.option('--file', help='Путь к файлу JSON для сохранения и чтения данных')
def main(file):
    data_file = file if file else click.prompt('Введите расположение файла:', type=str)
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

    lst_planes = load_data(data_file, schema)

    while True:
        menu(lst_planes, data_file, schema)


def load_data(data_file, schema):
    data = []
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            data = json.load(file)
            validate(data, schema)
    return data


def save_data(data, data_file, schema):
    validate(data, schema)
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)


def exit_to_program(data, data_file, schema):
    print('Всего доброго!')
    save_data(data, data_file, schema)
    exit(1)


def help_program():
    print("add - добавление рейса\n"
          "help - помощь по командам\n"
          "select \"пункт назначения\" - вывод самолетов летящих в п.н.\n"
          "display_plane - вывод всех самолетов\n"
          "exit - выход из программы")


def add_program(planes):
    plane = dict()
    plane["destination"] = click.prompt("Пункт назначения:")
    plane["flight_number"] = int(click.prompt("Номер рейса:", type=int))
    plane["type_plane"] = click.prompt("Тип самолета:")
    planes.append(plane)
    planes.sort(key=lambda key_plane: key_plane.get("flight_number"))
    return planes


def select_program(planes):
    lst = list(map(lambda x: x.get("destination"), planes))
    point = click.prompt('Выберите нужное вам место:')
    print("Результаты поиска")
    if point in lst:
        print('Рейсы в эту точку')
        for i in planes:
            if point == i["destination"]:
                print(f"{i['flight_number']}........{i['type_plane']}")
    else:
        print("Рейсов не найдено")


def error():
    print('Неверная команда')


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
                "Рейс"
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
        print("Рейсов не найдено")


def menu(lst_plane, data_file, schema):
    command = click.prompt('Введите команду ("help" - руководство по командам):').lower()
    if command == 'exit':
        exit_to_program(lst_plane, data_file, schema)
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
    main()
