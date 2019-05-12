import numpy as np
# import scipy.optimize as opt


class GameOnSphere(object):
    """Класс игры поиск на сфере
    point_number - количество точек 1 игрока
    epsilon - расстояние от 1 игрока, на котором 2 игрок считется найденным
    """
    def __init__(self, point_number=0, epsilon=0, radius=0):
        self.point_number = point_number
        self.radius = radius
        self.max_distance = epsilon / np.sin((np.pi - np.arcsin(epsilon / self.radius)) / 2)

    def get_point_on_sphere(self):
        z = np.random.uniform(-self.radius, self.radius)
        phi = np.random.uniform(0, 2 * np.pi)
        phi = 0 if phi == 2 * np.pi else phi

        r = np.sqrt(1 - z ** 2)
        x = np.cos(phi) * r
        y = np.sin(phi) * r

        return np.array([x, y, z])

    # @staticmethod
    # def get_point_on_sphere():
    #     """Возвращает координаты точки на единичной сфере с центром в (1, 1, 1)
    #     """
    #     def f(variables):
    #         """Возвращает систему функций, необходимых для нахождения точки
    #         на поверхности сферы
    #         """
    #         x, y, z = variables
    #
    #         if z > 1:
    #             eq1 = (x - 1) ** 2 + (y - 1) ** 2 + (np.sqrt(z - 1)) ** 2 - 1
    #         else:
    #             eq1 = (x - 1) ** 2 + (y - 1) ** 2 + (np.sqrt(1 - z)) ** 2 - 1
    #         eq2 = (x - 1) * (p_y - 1) - (y - 1) * (p_x - 1)
    #         eq3 = (z - 1) * (p_y - 1) - (y - 1) * (p_z - 1)
    #         return [eq1, eq2, eq3]
    #
    #     p_x = 0
    #     p_y = 0
    #     p_z = 0
    #     while (p_x - 1) ** 2 + (p_y - 1) ** 2 + (p_z - 1) ** 2 > 1:
    #         p_x = np.random.uniform(0, 2)
    #         p_y = np.random.uniform(0, 2)
    #         p_z = np.random.uniform(0, 2)
    #
    #     return opt.fsolve(f, (1, 1, 1))

    def get_points_for_player(self, name=""):
        points_list = []
        if name == "A":
            for i in range(self.point_number):
                points_list.append(self.get_point_on_sphere())
        elif name == "B":
            points_list.append(self.get_point_on_sphere())

        return points_list

    def win_function(self, player_a, player_b):
        win_a = False

        p_b = player_b[0]
        for p_a in player_a:
            distance = np.sqrt(np.sum((p_a - p_b) ** 2))
            if distance <= self.max_distance:
                win_a = True

        return win_a

    def start_game(self):
        player_a = self.get_points_for_player("A")
        player_b = self.get_points_for_player("B")

        return self.win_function(player_a, player_b)


def print_result(n, e, count_iterations):
    win_a = 0
    game = GameOnSphere(n, e, 1)
    for i in range(0, count_iterations):
        if game.start_game():
            win_a += 1

    print("Game on sphere, where player A with {0} points, epsilon = {1}:".format(n, e))

    numerical_result = win_a / count_iterations
    print("Player A win: {0: <3.4f}".format(numerical_result))
    print("Player B win: {0: <3.4f}".format(1 - numerical_result))

    analitic_result = n / 2 * (1 - np.sqrt(1 - e ** 2))
    print("Result of analitic method: {0: <3.4f}".format(analitic_result))
    print("Comparison of methods: {0: <3.4f}".format(np.abs(analitic_result - numerical_result)))
    print()


if __name__ == "__main__":
    # for n in np.arange(10, 40, 10):
    #    for e in np.arange(0.3, 0.8, 0.2):
    print_result(10, 0.2, 10000)
    print_result(5, 0.4, 10000)
