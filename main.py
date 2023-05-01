"""
Лабораторная работа 1 по ЛОИС.
Вариант 1Е (Проверка форумлы на КНФ)
Выполнили Никита Шахнович, Кирилл Акулич и Иван Титлов.
Дата выполнения: 17.03.2023
"""

TESTS = ["(A/\(((!B)/\(C/\D)))/\E)",
         "(A/\(((!B)/\(C/\D))/\E))",
         "((A\/B)/\((B\/C)/\(F\/D)))",
         "(A/\(((B\/C)\/F)/\K))"]


class CheckSCNF:
    ALPHABET = "()/\\!ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    AVAILABLE_VARS_SYMBOLS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    CONJUNCTION = '/\\'
    DISJUNCTION = "\\/"

    def __init__(self, expression: str) -> None:
        self.expression = expression

    def is_scnf(self) -> bool:
        """Основной метод, проверяющий функцию на СДНФ"""
        # Проверяем, не является ли формула пустой строкой
        if not self.expression: return False

        # Проверяем, что все символы из формулы находятся в алфавите
        if not all(x in self.ALPHABET for x in self.expression):
            return False
        # Проверяем количество скобок
        if self.expression.count(')') != self.expression.count(self.DISJUNCTION) + self.expression.count(
                self.CONJUNCTION) + self.expression.count("!"):
            return False
        # Проверяем формулу на грамматику
        if len(self.expression) > 1 and not self.grammar_check(self.expression): return False

        # Разделяем на конституенты по знаку конъюкции
        disjunctions_list = self.expression.split(self.CONJUNCTION)
        # Проверка конституент
        return self.check_constituents(disjunctions_list)

    def grammar_check(self, expression):
        '''Грамматическая проверка формулы'''
        if len(expression) == 1: return True
        copy = expression
        while True:
            closed_bracket = copy.find(')')
            if closed_bracket == -1:
                break
            # проверяет, что знак операции отрицания стоит только перед переменной
            if copy[closed_bracket - 2] == '!' and copy[closed_bracket - 1] not in self.AVAILABLE_VARS_SYMBOLS:
                return False
            # проверяет, что операция отрицания находится в ()
            if copy[closed_bracket - 2] == '!' and copy[closed_bracket - 3] == '(':
                # если находится, то (!<переменная>) заменяется на '0'
                copy = copy.replace(copy[closed_bracket - 3: closed_bracket + 1], '0')
            # проверяет, что бинарные операции с операндами находятся в ()
            elif copy[closed_bracket - 3: closed_bracket - 1] in (CheckSCNF.DISJUNCTION, CheckSCNF.CONJUNCTION) \
                    and copy[closed_bracket - 5] == '(':
                # если находится, то она заменяется на '0'
                copy = copy.replace(copy[closed_bracket - 5: closed_bracket + 1], '0')
            else:
                break
        # если осталась только '0', значит формула грамматически верна
        return copy == '0'

    @staticmethod
    def get_atomic_formuls(expression: str) -> list:
        """Получить список атомарных формул из логической формулы"""
        # Удаляем скобки и операции отрицания из формулы
        expression = expression.replace('(', '').replace(')', '').replace('!', '')
        # Разделяем выращение по оператору конъюнкции
        return expression.split(CheckSCNF.DISJUNCTION)

    @staticmethod
    def get_formuls_in_constituent(expression: str) -> list:
        """Получить список формул, разделенных конъюнкцией"""
        # Удаляем скобки из формулы
        expression = expression.replace('(', '').replace(')', '')
        # Разделяем выражение по оператору конъюнкции
        return expression.split(CheckSCNF.DISJUNCTION)

    def check_constituents(self, constituent_list: list) -> bool:
        """Проверка дизъюнкций"""
        # если одна конституента
        if len(constituent_list) > 1:
            # проверяем каждую из конституент на грамматику
            for set_index, set in enumerate(constituent_list):
                if set.count(CheckSCNF.DISJUNCTION) == 1:
                    if not self.grammar_check(set[set.rfind("("):set.find(")")+1]):
                        return False
                elif set.count(CheckSCNF.DISJUNCTION) > 1:
                    if set_index == len(constituent_list)-1:
                        if not self.grammar_check(set[:-1]):
                            return False
                    elif set_index == 0:
                        if not self.grammar_check(set[1:]):
                            return False
                    else:
                        if set.count("(") > set.count(")"):
                            if not self.grammar_check(set[1:]):
                                return False
                        elif set.count("(") < set.count(")"):
                            if not self.grammar_check(set[:-1]):
                                return False
                        else:
                            if not self.grammar_check(set):
                                return False
        return True


if __name__ == '__main__':
    while True:
        formula = input('Введите формулу:\t')
        if formula == "end":
            break
        if CheckSCNF(formula).is_scnf():
            print(f'{formula} является КНФ\n')
        else:
            print(f'{formula} не является КНФ\n')
