from abc import ABC, abstractmethod
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class GeometricFigure(ABC):
    @abstractmethod
    def area(self):
        pass

    @classmethod
    @abstractmethod
    def figure_name(cls):
        pass

class FigureColor:
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        # Здесь можно добавить проверку цвета
        self._color = value

class Rectangle(GeometricFigure):
    figure_type = "Прямоугольник"

    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color_obj = FigureColor(color)

    def area(self):
        return self.width * self.height

    @property
    def color(self):
        return self.color_obj.color

    @color.setter
    def color(self, value):
        self.color_obj.color = value

    @classmethod
    def figure_name(cls):
        return cls.figure_type

    def info(self):
        return ("Фигура: {name}, цвет: {color}, ширина: {w}, \n высота: {h}, "
                "площадь: {area:.2f}").format(
                    name=self.figure_name(),
                    color=self.color,
                    w=self.width,
                    h=self.height,
                    area=self.area()
                )

    def draw_rectangle(self, filename):
        fig, ax = plt.subplots()
        rect_patch = patches.Rectangle((0, 0), self.width, self.height,
                                       linewidth=2, edgecolor='black', facecolor=self.color)
        ax.add_patch(rect_patch)
        ax.set_xlim(-1, self.width + 1)
        ax.set_ylim(-1, self.height + 1)
        ax.set_aspect('equal')
        plt.title(self.info())

        if filename:
            fig.savefig(filename)
            print(f"Изображение сохранено в {filename}")

        plt.show()

class IsoscelesTrapezoid(GeometricFigure):
    figure_type = "Равнобедренная трапеция"

    def __init__(self, base, side, angle_deg, color):
        self.base = base
        self.side = side
        self.angle_deg = angle_deg
        self.color_obj = FigureColor(color)

    def area(self):
        Y_rad = math.radians(self.angle_deg)
        h = self.side * math.sin(Y_rad)
        c = self.base - 2 * self.side * math.cos(Y_rad)
        if c < 0:
            raise ValueError("Второе основание получается отрицательным — проверьте входные данные")
        return (self.base + c) / 2 * h

    @property
    def color(self):
        return self.color_obj.color

    @color.setter
    def color(self, value):
        self.color_obj.color = value

    @classmethod
    def figure_name(cls):
        return cls.figure_type

    def info(self):
        return ("Фигура: {name}, цвет: {color}, основание a: {a}, \nбоковая сторона b: {b}, "
                "угол Y: {Y}°, площадь: {area:.2f}").format(
                    name=self.figure_name(),
                    color=self.color,
                    a=self.base,
                    b=self.side,
                    Y=self.angle_deg,
                    area=self.area()
                )

    def draw_isosceles_trapezoid(self, filename):
        fig, ax = plt.subplots()

        Y_rad = math.radians(self.angle_deg)
        h = self.side * math.sin(Y_rad)
        c = self.base - 2 * self.side * math.cos(Y_rad)
        if c < 0:
            raise ValueError("Второе основание получается отрицательным — проверьте входные данные")


        points = [(0, 0), (self.base, 0), (self.base - c, h), (c, h)]

        polygon = patches.Polygon(points, closed=True, linewidth=2, edgecolor='black', facecolor=self.color)
        ax.add_patch(polygon)

        ax.set_xlim(-1, self.base + 1)
        ax.set_ylim(-1, h + 1)
        ax.set_aspect('equal')
        plt.title(self.info())

        if filename:
            fig.savefig(filename)
            print(f"Изображение сохранено в {filename}")

        plt.show()