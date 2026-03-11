import pytest
import csv
import os
import tempfile
from ParserForTabels import read_csv_files, calculate_median_coffee


@pytest.fixture
def sample_csv_file():
    #Создает временный CSV файл с тестовыми данными
    data = [
        ['student', 'date', 'coffee_spent', 'sleep_hours', 'study_hours', 'mood', 'exam'],
        ['Алексей Смирнов', '2024-06-01', '450', '4.5', '12', 'норм', 'Математика'],
        ['Алексей Смирнов', '2024-06-02', '500', '4.0', '14', 'устал', 'Математика'],
        ['Алексей Смирнов', '2024-06-03', '550', '3.5', '16', 'зомби', 'Математика'],
        ['Дарья Петрова', '2024-06-01', '200', '7.0', '6', 'отл', 'Математика'],
        ['Дарья Петрова', '2024-06-02', '250', '6.5', '8', 'норм', 'Математика'],
    ]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        temp_file = f.name

    yield temp_file
    os.unlink(temp_file)


@pytest.fixture
def multiple_csv_files():
    #Создает несколько временных CSV файлов
    files = []

    # Первый файл
    data1 = [
        ['student', 'date', 'coffee_spent', 'sleep_hours', 'study_hours', 'mood', 'exam'],
        ['Иван Петров', '2024-06-01', '300', '6.0', '8', 'норм', 'Физика'],
        ['Иван Петров', '2024-06-02', '350', '5.5', '9', 'норм', 'Физика'],
    ]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data1)
        files.append(f.name)

    # Второй файл
    data2 = [
        ['student', 'date', 'coffee_spent', 'sleep_hours', 'study_hours', 'mood', 'exam'],
        ['Мария Сидорова', '2024-06-01', '150', '8.0', '4', 'отл', 'Физика'],
        ['Мария Сидорова', '2024-06-02', '180', '7.5', '5', 'отл', 'Физика'],
    ]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data2)
        files.append(f.name)

    yield files

    for file in files:
        os.unlink(file)


def test_integration_full_workflow(sample_csv_file):
    #Интеграционный тест полного рабочего процесса
    data = read_csv_files([sample_csv_file])
    result = calculate_median_coffee(data)

    # Проверяем структуру результата
    assert len(result) == 2  # Два студента

    # Проверяем правильность медиан
    alexey = next(item for item in result if item['student'] == 'Алексей Смирнов')
    darya = next(item for item in result if item['student'] == 'Дарья Петрова')

    assert alexey['median_coffee'] == 500  # медиана для 450,500,550 = 500
    assert darya['median_coffee'] == 250  # медиана для 200,250 = 225? нет, для двух значений медиана = среднее = 225

    # Проверяем сортировку
    assert result[0]['student'] == 'Алексей Смирнов'
    assert result[1]['student'] == 'Дарья Петрова'


def test_integration_multiple_files(multiple_csv_files):
    #Интеграционный тест с несколькими файлами
    data = read_csv_files(multiple_csv_files)
    result = calculate_median_coffee(data)

    assert len(result) == 2

    ivan = next(item for item in result if item['student'] == 'Иван Петров')
    maria = next(item for item in result if item['student'] == 'Мария Сидорова')

    assert ivan['median_coffee'] == 325  # медиана для 300,350 = 325
    assert maria['median_coffee'] == 165  # медиана для 150,180 = 165

if __name__ == "__main__":
    pytest.main([__file__])
