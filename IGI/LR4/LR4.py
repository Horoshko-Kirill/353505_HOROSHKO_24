import csv
import pickle
import re
import zipfile
from collections import defaultdict
import math
import matplotlib.pyplot as plt
from statistics import mean, median, mode, pstdev, pvariance
import matplotlib.patches as patches
import numpy as np
from abc import ABC, abstractmethod


# Базовый класс с примесью (Mixin)
class StatsMixin:
    """Примесь для добавления статистических методов"""

    def calculate_stats(self, data):
        return {
            'mean': mean(data),
            'median': median(data),
            'mode': mode(data),
            'variance': pvariance(data),
            'std_dev': pstdev(data)
        }


# Абстрактный базовый класс
class BaseManager(ABC):
    """Абстрактный базовый класс для менеджеров данных"""
    # Статический атрибут
    DATA_FORMATS = ['csv', 'pickle', 'json']

    def __init__(self, data=None):
        # Динамический атрибут
        self.created_at = "2023-11-15"
        self.data = data or {}

    @abstractmethod
    def save(self, filename):
        pass

    @abstractmethod
    def load(self, filename):
        pass

    # Магический метод
    def __str__(self):
        return f"{self.__class__.__name__} with {len(self.data)} items"

    # Магический метод для доступа по индексу
    def __getitem__(self, key):
        return self.data[key]

    # Магический метод для итерации
    def __iter__(self):
        return iter(self.data.items())


class StudentManager(BaseManager, StatsMixin):
    """Класс для управления студентами с наследованием и примесью"""
    # Статический атрибут
    MIN_EXPERIENCE = 2

    def __init__(self, data=None):
        super().__init__(data)
        # Динамический атрибут
        self.modified = False

    def save(self, filename):
        ext = filename.split('.')[-1]
        if ext == 'csv':
            self.save_to_csv(filename)
        elif ext == 'pickle':
            self.save_to_pickle(filename)
        else:
            raise ValueError("Unsupported format")
        self.modified = False

    def load(self, filename):
        ext = filename.split('.')[-1]
        if ext == 'csv':
            self.load_from_csv(filename)
        elif ext == 'pickle':
            self.load_from_pickle(filename)
        else:
            raise ValueError("Unsupported format")
        self.modified = False

    def save_to_csv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Фамилия", "Нуждается в общежитии", "Стаж работы", "Окончил", "Язык"])
            for student_id, info in self.data.items():
                writer.writerow([
                    student_id,
                    info["surname"],
                    info["needs_hostel"],
                    info.get("work_experience", 0),
                    info["graduated_from"],
                    info["language"]
                ])

    def load_from_csv(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.data = {}
            for row in reader:
                self.data[row["ID"]] = {
                    "surname": row["Фамилия"],
                    "needs_hostel": row["Нуждается в общежитии"] == "True",
                    "work_experience": int(row["Стаж работы"]),
                    "graduated_from": row["Окончил"],
                    "language": row["Язык"]
                }

    def save_to_pickle(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_pickle(self, filename):
        with open(filename, 'rb') as file:
            self.data = pickle.load(file)

    @property
    def hostel_needed_count(self):
        """Свойство для подсчета нуждающихся в общежитии"""
        return sum(1 for student in self.data.values() if student["needs_hostel"])

    def get_experienced_students(self, min_experience=None):
        min_exp = min_experience or self.MIN_EXPERIENCE
        return [student["surname"] for student in self.data.values()
                if student.get("work_experience", 0) > min_exp]

    def get_technical_school_graduates(self):
        return [student["surname"] for student in self.data.values()
                if student["graduated_from"] == "техникум"]

    def get_language_groups(self):
        groups = defaultdict(list)
        for student in self.data.values():
            groups[student["language"]].append(student["surname"])
        return dict(groups)

    def search_student(self, surname):
        for info in self.data.values():
            if info["surname"].lower() == surname.lower():
                return info
        return None

    # Перегрузка оператора +
    def __add__(self, other):
        if isinstance(other, StudentManager):
            new_data = {**self.data, **other.data}
            return StudentManager(new_data)
        raise TypeError("Can only merge with another StudentManager")


class TextAnalyzer(BaseManager, StatsMixin):
    """Класс для анализа текста с полиморфизмом"""

    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            super().__init__(file.read())
        self._cache = {}  # Для кеширования результатов

    def save(self, filename):
        raise NotImplementedError("TextAnalyzer doesn't support save operation")

    def load(self, filename):
        raise NotImplementedError("TextAnalyzer doesn't support load operation")

    @property
    def sentences(self):
        if 'sentences' not in self._cache:
            self._cache['sentences'] = [s for s in re.split(r'[.!?]+', self.data) if s.strip()]
        return self._cache['sentences']

    def count_sentences(self):
        return len(self.sentences)

    def count_sentence_types(self):
        narrative = len(re.findall(r'[^.!?]*[.]', self.data))
        interrogative = len(re.findall(r'[^.!?]*[?]', self.data))
        imperative = len(re.findall(r'[^.!?]*[!]', self.data))
        return narrative, interrogative, imperative

    def avg_sentence_length(self):
        words = [word for s in self.sentences for word in re.findall(r'\w+', s)]
        return sum(len(word) for word in words) / len(words) if words else 0

    # Остальные методы класса TextAnalyzer остаются без изменений


class Figure:
    """Класс для работы с фигурами с использованием полиморфизма"""

    def __init__(self, **kwargs):
        self.color = kwargs.get('color', 'blue')
        self.label = kwargs.get('label', '')
        self._area = None  # Кеширование площади

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    def description(self):
        return f"Фигура: {self.__class__.__name__}\nЦвет: {self.color}\nПлощадь: {self.area():.2f}"

    # Магический метод для сравнения по площади
    def __lt__(self, other):
        if isinstance(other, Figure):
            return self.area() < other.area()
        return NotImplemented


class Rectangle(Figure):
    """Класс прямоугольника с наследованием"""

    def __init__(self, width, height, **kwargs):
        super().__init__(**kwargs)
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
        self._area = None

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value
        self._area = None

    def area(self):
        if self._area is None:
            self._area = self.width * self.height
        return self._area

    def draw(self):
        plt.figure()
        ax = plt.gca()
        ax.add_patch(plt.Rectangle((0, 0), self.width, self.height, color=self.color))
        plt.text(self.width / 2, self.height / 2, self.label, ha='center', va='center', color='white')
        plt.xlim(-1, self.width + 2)
        plt.ylim(-1, self.height + 2)
        plt.title("Прямоугольник")
        plt.grid(True)
        plt.gca().set_aspect('equal')
        plt.show()


class Trapezoid(Figure):
    """Класс трапеции с наследованием"""

    def __init__(self, a, b, angle_deg, **kwargs):
        super().__init__(**kwargs)
        self.a = a
        self.b = b
        self.angle_deg = angle_deg

    def area(self):
        h = self.b * math.sin(math.radians(self.angle_deg))
        return 0.5 * (self.a + self.a) * h

    def draw(self):
        plt.figure()
        ax = plt.gca()
        angle_rad = math.radians(self.angle_deg)
        h = self.b * math.sin(angle_rad)
        dx = self.b * math.cos(angle_rad)
        points = [(0, 0), (self.a, 0), (self.a - dx, h), (dx, h)]
        trapezoid = patches.Polygon(points, closed=True, color=self.color)
        ax.add_patch(trapezoid)
        plt.text(self.a / 2, h / 2, self.label, ha='center', va='center', color='white')
        plt.xlim(-1, self.a + 2)
        plt.ylim(-1, h + 2)
        plt.title("Трапеция")
        plt.grid(True)
        plt.gca().set_aspect('equal')
        plt.show()


# Демонстрация полиморфизма
def print_figure_info(figure):
    print(figure.description())
    figure.draw()


def main_menu():
    while True:
        print("\n" + "=" * 50)
        print("ГЛАВНОЕ МЕНЮ".center(50))
        print("=" * 50)
        print("1. Работа со студентами")
        print("2. Анализ текста")
        print("3. Работа с рядом ln(1-x)")
        print("4. Работа с геометрическими фигурами")
        print("5. Работа с матрицами")
        print("0. Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            student_menu()
        elif choice == "2":
            text_analyzer_menu()
        elif choice == "3":
            ln_series_menu()
        elif choice == "4":
            figures_menu()
        elif choice == "5":
            matrix_menu()
        elif choice == "0":
            print("Выход из программы...")
            break
        else:
            print("Неверный ввод, попробуйте снова")


def student_menu():
    students_data = {
        "1": {"surname": "Иванов", "needs_hostel": True, "work_experience": 0,
              "graduated_from": "школа", "language": "английский"},
        "2": {"surname": "Петров", "needs_hostel": False, "work_experience": 3,
              "graduated_from": "техникум", "language": "немецкий"},
    }
    manager = StudentManager(students_data)

    while True:
        print("\n" + "-" * 50)
        print("МЕНЮ РАБОТЫ СО СТУДЕНТАМИ".center(50))
        print("-" * 50)
        print("1. Показать всех студентов")
        print("2. Добавить студента")
        print("3. Поиск студента по фамилии")
        print("4. Статистика по студентам")
        print("5. Сохранить в файл")
        print("6. Загрузить из файла")
        print("0. Назад")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            print("\nСписок студентов:")
            for id, info in manager:
                print(f"{id}: {info['surname']} ({info['language']})")

        elif choice == "2":
            print("\nДобавление нового студента:")
            student_id = input("Введите ID: ")
            surname = input("Введите фамилию: ")
            needs_hostel = input("Нуждается в общежитии (да/нет): ").lower() == "да"
            work_experience = int(input("Стаж работы (лет): "))
            graduated_from = input("Окончил (школа/техникум): ")
            language = input("Язык: ")

            manager.data[student_id] = {
                "surname": surname,
                "needs_hostel": needs_hostel,
                "work_experience": work_experience,
                "graduated_from": graduated_from,
                "language": language
            }
            print("Студент добавлен!")

        elif choice == "3":
            surname = input("Введите фамилию для поиска: ")
            student = manager.search_student(surname)
            if student:
                print("\nНайден студент:")
                print(student)
            else:
                print("Студент не найден")

        elif choice == "4":
            print("\nСтатистика:")
            print(f"Нуждаются в общежитии: {manager.hostel_needed_count}")
            print(f"Окончили техникум: {len(manager.get_technical_school_graduates())}")
            print("Языковые группы:")
            for lang, students in manager.get_language_groups().items():
                print(f"{lang}: {len(students)} студентов")

        elif choice == "5":
            filename = input("Введите имя файла (csv или pkl): ")
            try:
                manager.save(filename)
                print("Данные сохранены!")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "6":
            filename = input("Введите имя файла для загрузки: ")
            try:
                manager.load(filename)
                print("Данные загружены!")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "0":
            break
        else:
            print("Неверный ввод, попробуйте снова")


def text_analyzer_menu():
    while True:
        print("\n" + "-" * 50)
        print("МЕНЮ АНАЛИЗА ТЕКСТА".center(50))
        print("-" * 50)
        print("1. Анализировать файл")
        print("2. Показать статистику")
        print("0. Назад")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            filename = input("Введите путь к файлу: ")
            try:
                analyzer = TextAnalyzer(filename)
                print("\nАнализ завершен!")
                print(f"Количество предложений: {analyzer.count_sentences()}")

                # Сохраняем результаты
                save_results(analyzer, "text_analysis_results.txt")
                create_zip("text_analysis_results.txt", "text_analysis.zip")

            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "2":
            try:
                with open("text_analysis_results.txt", "r", encoding="utf-8") as f:
                    print(f.read())
            except FileNotFoundError:
                print("Сначала проанализируйте файл")

        elif choice == "0":
            break
        else:
            print("Неверный ввод, попробуйте снова")


def ln_series_menu():
    while True:
        print("\n" + "-" * 50)
        print("МЕНЮ РАБОТЫ С РЯДОМ LN(1-X)".center(50))
        print("-" * 50)
        print("1. Вычислить ряд для конкретного x")
        print("2. Построить график для диапазона x")
        print("0. Назад")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            try:
                x = float(input("Введите x (0 < x < 1): "))
                eps = float(input("Введите точность (например, 0.0001): "))

                ln_series = LnSeries(x, eps)
                print("\nРезультаты:")
                print(f"Вычисленное значение: {ln_series.fx}")
                print(f"Значение через math.log: {ln_series.math_fx}")
                print(f"Ошибка: {ln_series.error}")
                print(f"Количество итераций: {ln_series.n}")

                stats = ln_series.stats()
                print("\nСтатистика по членам ряда:")
                for k, v in stats.items():
                    print(f"{k}: {v}")

            except ValueError as e:
                print(f"Ошибка ввода: {e}")

        elif choice == "2":
            try:
                eps = float(input("Введите точность (например, 0.0001): "))
                xs = [i / 100 for i in range(1, 99)]  # x от 0.01 до 0.98
                series_values = []
                math_values = []

                for x in xs:
                    ln_series = LnSeries(x, eps)
                    series_values.append(ln_series.fx)
                    math_values.append(ln_series.math_fx)

                plt.figure(figsize=(10, 6))
                plt.plot(xs, series_values, label='Разложение ln(1 - x)', color='blue')
                plt.plot(xs, math_values, label='math.log(1 - x)', color='red', linestyle='--')
                plt.title('Сравнение разложения ln(1 - x) и math.log(1 - x)')
                plt.xlabel('x')
                plt.ylabel('ln(1 - x)')
                plt.legend()
                plt.grid(True)
                plt.show()

            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "0":
            break
        else:
            print("Неверный ввод, попробуйте снова")


def figures_menu():
    while True:
        print("\n" + "-" * 50)
        print("МЕНЮ РАБОТЫ С ФИГУРАМИ".center(50))
        print("-" * 50)
        print("1. Создать прямоугольник")
        print("2. Создать трапецию")
        print("3. Сравнить фигуры по площади")
        print("0. Назад")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            try:
                width = float(input("Ширина: "))
                height = float(input("Высота: "))
                color = input("Цвет: ")
                label = input("Подпись: ")

                rect = Rectangle(width, height, color=color, label=label)
                print("\nПрямоугольник создан!")
                print(rect.description())
                rect.draw()

            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == "2":
            try:
                a = float(input("Основание: "))
                b = float(input("Боковая сторона: "))
                angle = float(input("Угол (в градусах): "))
                color = input("Цвет: ")
                label = input("Подпись: ")

                trap = Trapezoid(a, b, angle, color=color, label=label)
                print("\nТрапеция создана!")
                print(trap.description())
                trap.draw()

            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == "3":
            try:
                print("\nСоздайте первую фигуру:")
                type1 = input("Тип (1-прямоугольник, 2-трапеция): ")

                if type1 == "1":
                    w = float(input("Ширина: "))
                    h = float(input("Высота: "))
                    fig1 = Rectangle(w, h)
                else:
                    a = float(input("Основание: "))
                    b = float(input("Боковая сторона: "))
                    angle = float(input("Угол: "))
                    fig1 = Trapezoid(a, b, angle)

                print("\nСоздайте вторую фигуру:")
                type2 = input("Тип (1-прямоугольник, 2-трапеция): ")

                if type2 == "1":
                    w = float(input("Ширина: "))
                    h = float(input("Высота: "))
                    fig2 = Rectangle(w, h)
                else:
                    a = float(input("Основание: "))
                    b = float(input("Боковая сторона: "))
                    angle = float(input("Угол: "))
                    fig2 = Trapezoid(a, b, angle)

                print("\nРезультат сравнения:")
                print(f"Площадь первой фигуры: {fig1.area():.2f}")
                print(f"Площадь второй фигуры: {fig2.area():.2f}")
                print(f"Первая фигура {'меньше' if fig1 < fig2 else 'не меньше'} второй")

            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == "0":
            break
        else:
            print("Неверный ввод, попробуйте снова")


def matrix_menu():
    while True:
        print("\n" + "-" * 50)
        print("МЕНЮ РАБОТЫ С МАТРИЦАМИ".center(50))
        print("-" * 50)
        print("1. Создать случайную матрицу")
        print("2. Найти максимумы в столбцах")
        print("3. Поменять местами максимумы")
        print("4. Вычислить статистику")
        print("5. Вычислить корреляцию")
        print("0. Назад")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            try:
                n = int(input("Количество строк: "))
                m = int(input("Количество столбцов: "))
                A = np.random.randint(1, 100, size=(n, m))
                print("\nМатрица создана:")
                print(A)

                # Сохраняем матрицу для использования в других пунктах
                np.save("matrix.npy", A)

            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice in ["2", "3", "4", "5"]:
            try:
                A = np.load("matrix.npy")
                print("\nТекущая матрица:")
                print(A)

                if choice == "2":
                    first_col = A[:, 0]
                    last_col = A[:, -1]
                    max_first = np.max(first_col)
                    max_last = np.max(last_col)
                    print(f"\nМаксимум в первом столбце: {max_first}")
                    print(f"Максимум в последнем столбце: {max_last}")

                elif choice == "3":
                    first_col = A[:, 0]
                    last_col = A[:, -1]
                    max_first_idx = np.argmax(first_col)
                    max_last_idx = np.argmax(last_col)

                    A[max_first_idx, 0], A[max_last_idx, -1] = A[max_last_idx, -1], A[max_first_idx, 0]
                    print("\nМатрица после замены:")
                    print(A)
                    np.save("matrix.npy", A)

                elif choice == "4":
                    print("\nСтатистика по матрице:")
                    print(f"Среднее: {np.mean(A):.2f}")
                    print(f"Медиана: {np.median(A):.2f}")
                    print(f"Дисперсия: {np.var(A):.2f}")
                    print(f"Стандартное отклонение: {np.std(A):.2f}")

                elif choice == "5":
                    corr = np.corrcoef(A[:, 0], A[:, -1])[0, 1]
                    print(f"\nКорреляция между первым и последним столбцами: {corr:.2f}")

            except FileNotFoundError:
                print("Сначала создайте матрицу")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "0":
            break
        else:
            print("Неверный ввод, попробуйте снова")


if __name__ == "__main__":
    main_menu()