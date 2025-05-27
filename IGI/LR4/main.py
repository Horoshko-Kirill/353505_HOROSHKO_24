from regular import Regular
from student import Student
from serialize import *
from function import *
from figure import *
from workwithnumpy import *
from catdataanalyzer import *


def main_menu():
    while True:
        print("\nВыберите задачу для выполнения:")
        print("1 - Task 1 ")
        print("2 - Task 2 ")
        print("3 - Task 3 ")
        print("4 - Task 4 ")
        print("5 - Task 5 ")
        print("6 - Task 6 ")
        print("0 - Выход")

        choice = input("Введите номер задачи (0-6): ").strip()

        if choice == '1':
            # Task 1
            print("\n--- Task 1 ---")
            dictionary = [
                {
                    "last_name": "Петров",
                    "dormitory": True,
                    "exp": 2,
                    "study": "bsuir",
                    "lang": "EN"
                },
                {
                    "last_name": "Иванов",
                    "dormitory": True,
                    "exp": 0,
                    "study": "bsuir",
                    "lang": "EN"
                },
                {
                    "last_name": "Логин",
                    "dormitory": False,
                    "exp": 10,
                    "study": "bsu",
                    "lang": "PL"
                },
                {
                    "last_name": "Пупкин",
                    "dormitory": False,
                    "exp": 0,
                    "study": "gsu",
                    "lang": "EN"
                },
                {
                    "last_name": "Охлабыстин",
                    "dormitory": True,
                    "exp": 5,
                    "study": "bsmu",
                    "lang": "EN"
                },
            ]

            student = []

            for data in dictionary:
                st = Student(data["last_name"], data["dormitory"], data["exp"], data["study"], data["lang"])
                student.append(st)

            for s in student:
                print(s)

            serialize_pickle = Serialize_Pickle()
            serialize_csv = Serialize_CSV()
            serialize_csv.print("student.csv", dictionary)
            serialize_pickle.print("student.pkl", student)
            print("Чтение из файла .csv")
            read_data = serialize_csv.read("student.csv")
            print(read_data)
            print("Чтение из файла .pkl")
            read_student = serialize_pickle.read("student.pkl")
            for s in read_student:
                print(s)

            students_with_exp = []
            sdutents_bsuir = []
            groups = {}

            for s in student:
                if s.exp >= 2:
                    students_with_exp.append(s)

                if s.study == "bsuir":
                    sdutents_bsuir.append(s)

                if s.lang not in groups:
                    groups[s.lang] = []
                    groups[s.lang].append(s)
                else:
                    groups[s.lang].append(s)

            print("2 года стажа и больше:")

            for s in students_with_exp:
                print(s)

            print("Учатся в БГУИР")

            for s in sdutents_bsuir:
                print(s)

            print("Языковые группы")

            for s in groups:
                print(s)
                for i in groups[s]:
                    print(i)

            while True:
                ans = input('Хотите выполнить поиск студента по фамилии? Y/N ').upper()
                if ans == 'Y':
                    last_name = input('Введите фамилию студента ')
                    flag = True
                    for s in student:
                        if s.last_name == last_name:
                            print(s)
                            flag = False
                            break
                    if flag:
                        print('Студент не найден')
                elif ans == 'N':
                    break
                else:
                    print('Не корректный ввод')

        elif choice == '2':
            # Task 2
            print("\n--- Task 2 ---")
            Regular.print_inf("input.txt", "output.txt")

            while True:
                ans = input('Хотите проверить MAC-адрес? Y/N ').upper()
                if ans == 'Y':
                    mac = input('Введите MAC-адрес ')
                    if Regular.isMAC(mac):
                        print("Это правильный MAC-адрес")
                    else:
                        print("Это не правильный MAC-адрес")
                elif ans == 'N':
                    break
                else:
                    print('Не корректный ввод')

        elif choice == '3':
            # Task 3
            print("\n--- Task 3 ---")
            s = Function()
            s.print()
            s.graph()

        elif choice == '4':
            # Task 4
            print("\n--- Task 4 ---")
            def input_float(prompt, positive=False):
                while True:
                    try:
                        val = float(input(prompt))
                        if positive and val <= 0:
                            print("Введите положительное число.")
                            continue
                        return val
                    except ValueError:
                        print("Некорректный ввод. Введите число.")

            print("Выберите фигуру:")
            print("1 - Прямоугольник")
            print("2 - Равнобедренная трапеция")

            choice_fig = input("Введите номер фигуры: ").strip()
            if choice_fig == '1':
                width = input_float("Введите ширину: ", positive=True)
                height = input_float("Введите высоту: ", positive=True)
                color = input("Введите цвет фигуры (например, 'blue', 'red'): ")
                filename = input("Введите имя файла для сохранения (например, 'rectangle.png'): ").strip()

                rect = Rectangle(width, height, color)
                rect.draw_rectangle(filename)
                print(rect.info())

            elif choice_fig == '2':
                base = input_float("Введите основание a: ", positive=True)
                side = input_float("Введите боковую сторону b: ", positive=True)
                angle_deg = input_float("Введите угол Y (в градусах, от 0 до 180): ")
                if not (0 < angle_deg < 180):
                    print("Угол должен быть в диапазоне от 0 до 180 градусов.")
                else:
                    color = input("Введите цвет фигуры (например, 'green', 'yellow'): ")
                    filename = input("Введите имя файла для сохранения (например, 'trapezoid.png'): ").strip()
                    try:
                        trap = IsoscelesTrapezoid(base, side, angle_deg, color)
                        trap.draw_isosceles_trapezoid(filename)
                        print(trap.info())
                    except ValueError as e:
                        print(f"Ошибка: {e}")

            else:
                print("Некорректный выбор фигуры.")

        elif choice == '5':
            # Task 5
            print("\n--- Task 5 ---")
            def input_positive_int(prompt):
                while True:
                    try:
                        value = int(input(prompt))
                        if value <= 0:
                            print("Ошибка: число должно быть положительным и больше нуля.")
                        else:
                            return value
                    except ValueError:
                        print("Ошибка: введите целое число.")

            def input_dimensions():
                print("Введите размеры матрицы:")
                m = input_positive_int("Количество строк (m): ")
                n = input_positive_int("Количество столбцов (n): ")
                return m, n

            m, n = input_dimensions()
            s = Task5(m, n)
            s.print()
            s.swap()

        elif choice == '6':
            # Task 6
            print("\n--- Task 6 ---")
            analyzer = CatDataAnalyzer("cat_breeds_clean.csv")

            while True:
                print("\n--- Меню ---")
                print("1. Показать информацию о DataFrame")
                print("2. Создать и отобразить Series по столбцу")
                print("3. Получить доступ к элементу Series")
                print("4. Сравнить средние значения по признаку и условию")
                print("5. Выйти")

                choice_inner = input("Выберите пункт (1-5): ").strip()
                if choice_inner == '1':
                    analyzer.show_dataframe_info()

                elif choice_inner == '2':
                    column = input("Введите имя столбца для Series: ").strip()
                    if column in analyzer.df.columns:
                        analyzer.create_series(column)
                        analyzer.show_series()
                    else:
                        print("Такого столбца нет в таблице.")

                elif choice_inner == '3':
                    if analyzer.series is None:
                        print("Сначала создайте Series.")
                        continue
                    try:
                        index = int(input("Введите индекс элемента Series: "))
                        analyzer.access_series_element(index)
                    except ValueError:
                        print("Ошибка: индекс должен быть целым числом.")

                elif choice_inner == '4':
                    value_column = input("Введите имя столбца для вычисления среднего значения: ").strip()
                    condition_column = input("Введите имя столбца для условия (min/max): ").strip()
                    if value_column not in analyzer.df.columns or condition_column not in analyzer.df.columns:
                        print("Один или оба столбца не найдены.")
                    else:
                        analyzer.compare_means_by_condition(value_column, condition_column)

                elif choice_inner == '5':
                    print("Возврат в главное меню.")
                    break

                else:
                    print("Неверный ввод. Введите число от 1 до 5.")

        elif choice == '0':
            print("Выход из программы. До свидания!")
            break

        else:
            print("Неверный ввод. Пожалуйста, введите число от 0 до 6.")


if __name__ == "__main__":
    main_menu()
