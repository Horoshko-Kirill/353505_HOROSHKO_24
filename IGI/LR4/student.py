
class Student:
    def __init__(self, last_name, dormitory, exp, study, lang):
        self.__last_name = last_name
        self.__dormitory = dormitory
        self.__exp = exp
        self.__study = study
        self.__lang = lang

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = last_name

    @property
    def dormitory(self):
        return self.__dormitory

    @dormitory.setter
    def dormitory(self, dormitory):
        self.__dormitory = dormitory

    @property
    def exp(self):
        return self.__exp

    @exp.setter
    def exp(self, exp):
        self.__exp = exp

    @property
    def study(self):
        return self.__study

    @study.setter
    def study(self, study):
        self.__study = study

    @property
    def lang(self):
        return self.__lang

    @lang.setter
    def lang(self, lang):
        self.__lang = lang

    def __str__(self):
        return (f"Фамилия: {self.__last_name}, "
                f"Общежитие: {self.dormitory}, "
                f"Стаж: {self.__exp}, "
                f"Окончил: {self.__study}, "
                f"Язык: {self.lang}")
