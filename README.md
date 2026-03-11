TestTask 
Тестовое задание 
Перед запуском программы сначала установите файл с зависимостями. Введите в консоль команду pip install -r requirements.txt 

Для запуска программы, если файлы лежат в той же папке что и код, введите в консоль команду python ParserForTabels.py --files math.csv physics.csv programming.csv --report median-coffee 
Если файлы лежат в другом месте, то вместо названий укажите путь python ParserForTabels.py --files data/math.csv data/physics.csv --report median-coffee 

Для запуска тестов, используйте следующие команды: 

Запуск всех тестов pytest test_coffee_report.py -v 

Запуск с подробным выводом pytest test_coffee_report.py -v --tb=short 

Запуск конкретного теста pytest test_coffee_report.py::test_integration_multiple_files -v
