import pandas as pd
from IPython.display import display


class CatDataAnalyzer:
    def __init__(self, file_path):

        self.df = pd.read_csv(file_path, delimiter=';')
        print("Файл успешно загружен.")

    def create_series(self, column_name):

        self.series = pd.Series(self.df[column_name])
        print(f"Серия по столбцу '{column_name}' создана.")

    def show_series(self, n=5):

        print(f"Первые {n} элементов Series:")
        display(self.series.head(n))

    def access_series_element(self, index):

        value_loc = self.series.loc[index]
        value_iloc = self.series.iloc[index]
        print(f"Элемент по loc[{index}]: {value_loc}")
        print(f"Элемент по iloc[{index}]: {value_iloc}")

    def show_dataframe_info(self):

        print("Информация о DataFrame:")
        self.df.info()
        print("\nСтатистики:")
        display(self.df.describe(include='all'))

    def compare_means_by_condition(self, target_column, condition_column):

        max_val = self.df[condition_column].max()
        min_val = self.df[condition_column].min()

        group_max = self.df[self.df[condition_column] == max_val]
        group_min = self.df[self.df[condition_column] == min_val]

        mean_max = group_max[target_column].mean()
        mean_min = group_min[target_column].mean()

        if mean_min == 0:
            print("Среднее значение для минимального значения — 0. Деление невозможно.")
            return None

        ratio = mean_max / mean_min
        print(f"Среднее значение '{target_column}' при максимальном '{condition_column}': {mean_max:.2f}")
        print(f"Среднее значение '{target_column}' при минимальном '{condition_column}': {mean_min:.2f}")
        print(f"Отношение: {ratio:.2f} раз(а)")
        return ratio
