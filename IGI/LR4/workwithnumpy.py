import numpy as np

class Task5:

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.A = np.random.randint(0, 101, size=(n, m))

    def print(self):
        print("Исходная матрица A:")
        print(self.A)

        mean_first_col = np.mean(self.A[:, 0])
        median_first_col = np.median(self.A[:, 0])
        var_first_col = np.var(self.A[:, 0])
        std_first_col = np.std(self.A[:, 0])

        print(f"\nСреднее значение первого столбца: {mean_first_col:.2f}")
        print(f"Медиана первого столбца: {median_first_col}")
        print(f"Дисперсия первого столбца: {var_first_col:.2f}")
        print(f"Стандартное отклонение первого столбца: {std_first_col:.2f}")

    def swap(self):
        max_first_idx = np.argmax(self.A[:, 0])
        max_last_idx = np.argmax(self.A[:, -1])

        print(f"\nМаксимальный элемент первого столбца: {self.A[max_first_idx, 0]} (строка {max_first_idx})")
        print(f"Максимальный элемент последнего столбца: {self.A[max_last_idx, -1]} (строка {max_last_idx})")

        self.A[max_first_idx, 0], self.A[max_last_idx, -1] = self.A[max_last_idx, -1], self.A[max_first_idx, 0]

        print("\nМатрица после обмена максимальных элементов:")
        print(self.A)

        corr_matrix = np.corrcoef(self.A[:, 0], self.A[:, -1])
        corr_coef = corr_matrix[0, 1]
        print(f"\nКоэффициент корреляции между первым и последним столбцами: {corr_coef:.2f}")

