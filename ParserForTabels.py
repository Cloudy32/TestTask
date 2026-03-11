import argparse
import csv
import statistics
from collections import defaultdict
from tabulate import tabulate
from typing import Any


def parse_arguments()-> Any:
    #Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description='Обработка данных о подготовке студентов к экзаменам')
    parser.add_argument('--files', nargs='+', required=True, help='Список CSV файлов для обработки')
    parser.add_argument('--report', required=True, choices=['median-coffee'],
                       help='Тип отчета (поддерживается только median-coffee)')
    return parser.parse_args()


def read_csv_files(file_list) -> Any:
    #Чтение данных из нескольких CSV файлов
    all_data = []

    for filename in file_list:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Проверяем наличие необходимых колонок
            if 'student' not in reader.fieldnames or 'coffee_spent' not in reader.fieldnames:
                print(f"Предупреждение: Файл {filename} не содержит необходимых колонок. Пропускаем.")
                continue

            for row in reader:
                # Преобразуем строковое значение coffee_spent в число

                    row['coffee_spent'] = float(row['coffee_spent'])
                    all_data.append(row)
                    continue

    return all_data


def calculate_median_coffee(data) -> list[dict]:
    # Расчет медианной суммы трат на кофе по каждому студенту

    # Группируем траты по студентам
    student_spending = defaultdict(list)

    for row in data:
        student = row['student']
        coffee_spent = row['coffee_spent']
        student_spending[student].append(coffee_spent)

    # Рассчитываем медиану для каждого студента
    result = []

    for student, spending in student_spending.items():
        median = statistics.median(spending)
        result.append({
            'student': student,
            'median_coffee': median
        })

    # Сортируем по убыванию медианных трат
    result.sort(key=lambda x: x['median_coffee'], reverse=True)

    return result


def main():
    args = parse_arguments()

    # Читаем данные из всех файлов
    data = read_csv_files(args.files)

    # Рассчитываем медианные траты на кофе
    result = calculate_median_coffee(data)

    # Формируем данные для таблицы
    table_data = [[item['student'], f"{item['median_coffee']:.2f}"] for item in result]
    headers = ['Студент', 'Медианные траты на кофе (руб)']

    # Выводим отчет(Добавил пару строк, для придания красоты)
    print("\n" + "=" * 60)
    print("ОТЧЕТ: Медианные траты на кофе за период сессии")
    print("=" * 60)
    print(tabulate(table_data, headers=headers, tablefmt='grid', numalign='right'))


if __name__ == '__main__':
    main()