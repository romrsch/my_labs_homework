from enum import Enum
import math
import random


def display_array(arr):
    """
    Метод для отображения изначальной матрицы
    :param arr:
    :return:
    """
    max_x = len(arr[0])  # Максимальная координата матрицы по X
    max_y = len(arr)  # Максимальная координата матрицы по Y

    for i in range(max_x):
        print("|", end="")
        for j in range(max_y):
            val = arr[i][j]
            print(f"{val:>2}|", end="")
        print()
    print("-" * 167)


def get_max_and_min(arr):
    """
    Метод для получения нижней и верхней цены игры
    :param arr:
    :return:
    """
    max_in_column = dict()
    min_in_row = dict()

    max_x = len(arr[0])  # Максимальная координата матрицы по X
    max_y = len(arr)  # Максимальная координата матрицы по Y

    for i in range(max_x):
        for j in range(max_y):
            val = arr[i][j]

            if not max_in_column.get(i):
                max_in_column[i] = -math.inf
            if max_in_column[i] < val:
                max_in_column[i] = val
            if not min_in_row.get(j):
                min_in_row[j] = math.inf
            if min_in_row[j] > val:
                min_in_row[j] = val

    a = max(min_in_row.values())
    b = min(max_in_column.values())
    return a, b


def get_optimal_strategy(arr):
    """
    Метод для получения оптимальной стратегии
    :param arr:
    :return:
    """
    b0 = arr[0][0] - arr[0][1]
    b1 = arr[1][0] - arr[1][1]
    p2 = 1 / (1 - (b1 / b0))
    p1 = 1 - p2
    v = arr[0][1] * p1 + arr[1][1] * p2
    return p1, p2, v


def ge_mixed_strategy(arr):
    """
    Метод для получения смешанной стратегии
    :param arr:
    :return:
    """
    b0 = arr[0][0] - arr[1][0]
    b1 = arr[0][1] - arr[1][1]
    q2 = 1.0 / (1 - (b1 / b0))
    q1 = 1 - q2
    v = arr[1][0] * q1 + arr[1][1] * q2
    return q1, q2, v


def game(arr, p1, q1):
    """
    Метод для запуска игры
    :param arr:
    :param p1:
    :param q1:
    :return:
    """
    parties = list()
    sum_win_a = 0
    for i in range(1, max_parties_count + 1):
        random_a = random.random()
        if random_a < p1:
            strategy_a = StrategyA.A1
        else:
            strategy_a = StrategyA.A2
        random_b = random.random()
        if random_b < q1:
            strategy_b = StrategyB.B1
        else:
            strategy_b = StrategyB.B2

        index_a = 0
        if strategy_a == StrategyA.A1:
            index_a = 0
        elif strategy_a == StrategyA.A2:
            index_a = 1

        index_b = 0
        if strategy_b == StrategyB.B1:
            index_b = 0
        elif strategy_b == StrategyB.B2:
            index_b = 1

        val = arr[index_a][index_b]
        sum_win_a += val
        avg_win_a = sum_win_a / i

        party = Party(i, random_a, strategy_a, random_b, strategy_b, val, sum_win_a, avg_win_a)
        parties.append(party)
    return parties


class StrategyA(Enum):
    """
    Нумерация стратегий игрока A
    """
    A1 = 0
    A2 = 1


class StrategyB(Enum):
    """
    Нумерация стратегий игрока B
    """
    B1 = 0
    B2 = 1


class Party:
    """
    Класс-обёртка для одной итерации игры
    """
    def __init__(self, PartyNumber, RandomA, StrategyA, RandomB, StrategyB, WinA, SumWinA, AvgWinA):
        self.PartyNumber = PartyNumber
        self.RandomA = RandomA
        self.StrategyA = StrategyA
        self.RandomB = RandomB
        self.StrategyB = StrategyB
        self.WinA = WinA
        self.SumWinA = SumWinA
        self.AvgWinA = AvgWinA


def main():
    print('Лабораторная работа №2. Вариант 8.')
    print('Моделирование матричной игры 2×2.\n')

    arr = [
        [5, 9],
        [10, 8]
    ]

    print("Исходная матрица:")
    display_array(arr)

    a, b = get_max_and_min(arr)

    print(f"a = [{a}], b = [{b}]")
    print("a <> b, следовательно, игра не имеет седловой точки, решение будет в смешанных стратегиях\n")

    print("Найдём оптимальную стратегию:")
    p1, p2, v1 = get_optimal_strategy(arr)
    print(f"p1 = [{p1:.2f}], p2 = [{p2:.2f}], v = [{v1:.2f}]\n")

    print("Найдём смешанную стратегию:")
    q1, q2, v2 = ge_mixed_strategy(arr)
    print(f"q1 = [{q1:.2f}], q2 = [{q2:.2f}], v = [{v2:.2f}]\n")

    print("100 партий игры:")
    parties = game(arr, p1, q1)
    print(f"|Номер партии|Случайное число для игрока А|Стратегия игрока А|Случайное число для игрока В|"
          f"Стратегия игрока В|Выигрыш игрока А|Накопленный выигрыш А|Средний выигрыш А|")

    print("-" * 167)
    for party in parties:
        print(f"|{party.PartyNumber:^12}|"
              f"{party.RandomA:^28.3f}|{party.StrategyA.name:^18}|"
              f"{party.RandomB:^28.3f}|{party.StrategyB.name:^18}|"
              f"{party.WinA:^16}|{party.SumWinA:^21}|{party.AvgWinA:^17.2f}|")
    print()

    a1Count = len([i.StrategyA for i in parties if i.StrategyA.name == "A1"])
    a2Count = len([i.StrategyA for i in parties if i.StrategyA.name == "A2"])
    b1Count = len([i.StrategyB for i in parties if i.StrategyB.name == "B1"])
    b2Count = len([i.StrategyB for i in parties if i.StrategyB.name == "B2"])

    freqP1 = a1Count / max_parties_count
    freqP2 = a2Count / max_parties_count
    freqQ1 = b1Count / max_parties_count
    freqQ2 = b2Count / max_parties_count

    print("Относительные частоты использования стратегий:")
    print(f"p = ({freqP1:.2f}(A1); {freqP2:.2f}(A2)), q = ({freqQ1:.2f}(B1); {freqQ2:.2f}(B2))")
    print()


if __name__ == "__main__":
    max_parties_count = 100  # Максимальное количество итераций игры
    main()
