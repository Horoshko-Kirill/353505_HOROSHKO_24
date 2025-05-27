import math
import numpy
import statistics
import matplotlib.pyplot as plt


class Function:

    x_vals = numpy.linspace(-0.99, 0.99, 200)
    n_terms = 20

    @staticmethod
    def ln1x(x, n):
        return sum([(-1) * x ** k / k for k in range(1, n + 1)])

    def __init__(self):
        self.series_vals = [self.ln1x(x, self.n_terms) for x in self.x_vals]
        self.math_vals = [math.log(1 - x) for x in self.x_vals]

        self.avg = statistics.mean(self.series_vals)
        self.median = statistics.median(self.series_vals)
        self.mode = statistics.mode(self.series_vals)
        self.variance = statistics.variance(self.series_vals)
        self.std = statistics.stdev(self.series_vals)

    def print(self):
        print(f"Среднее: {self.avg:.4f}")
        print(f"Медиана: {self.median:.4f}")
        print(f"Мода: {self.mode}")
        print(f"Дисперсия: {self.variance:.4f}")
        print(f"СКО: {self.std:.4f}")

    def graph(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.x_vals, self.series_vals, label=f"Ряд Тейлора (n={self.n_terms})", color='blue')
        plt.plot(self.x_vals, self.math_vals, label="math.log(1 - x)", color='red', linestyle='dashed')

        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)

        plt.title("Сравнение разложения ln(1 - x) и точной функции")
        plt.xlabel("x")
        plt.ylabel("ln(1 - x)")
        plt.legend()
        plt.grid(True)
        plt.savefig("graph.png")
        plt.show()
