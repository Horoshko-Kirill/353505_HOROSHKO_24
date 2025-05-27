
import csv
import pickle
from logger import LoggerMixin

class Serialize_CSV(LoggerMixin):
    def print(self, filename, data):
        try:
            with open(filename, 'w', newline='', encoding='cp1251') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys(), delimiter=';')
                writer.writeheader()
                writer.writerows(data)
            self.log("Выполнена запись в .csv файл")
        except Exception as e:
            self.log(e)

    def read(self, filename):
        try:
            with open(filename, 'r', encoding='cp1251') as f:
                reader = csv.DictReader(f, delimiter=';')
                data = [row for row in reader]
                self.log("Выполнено чтение из .csv файла")
                return data
        except Exception as e:
            self.log(e)
            return []


class Serialize_Pickle(LoggerMixin):
    def print(self, filename, list):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(list, file)
            self.log("Выполнена запись в .pkl файл")
        except Exception as e:
            self.log(e)

    def read(self, filename):
        try:
            with open(filename, 'rb') as file:
                list = pickle.load(file)
                self.log("Выполнено чтение из .pkl файла")
                return list
        except Exception as e:
            self.log(e)
