import numpy as np
import itertools


def check_super_additive(game):
    is_super_additive = True

    error_coal = []
    all_coalision = [set(k.split(" ")) for k in game.keys() if k != "" and k != "1 2 3 4"]
    for s, t in itertools.combinations(all_coalision, 2):
        if not s & t:
            key_s = " ".join(sorted(list(s)))
            key_t = " ".join(sorted(list(t)))
            key_st = " ".join(sorted(list(s | t)))

            if game[key_st] < game[key_s] + game[key_t]:
                is_super_additive = False
                error_coal.append(key_st)

    return is_super_additive, error_coal


def get_vector_shepli(game):
    all_coalision = [set(k.split(" ")) for k in game.keys() if k != ""]
    vector = np.zeros(5)

    for i in np.arange(1, 5):
        for coal in all_coalision:
            v_s = " ".join(sorted(list(coal)))
            v_s_i = " ".join(sorted(list(coal.difference(set(str(i))))))

            vector[i] += np.math.factorial(len(coal) - 1) * np.math.factorial(4 - len(coal)) * (game[v_s] - game[v_s_i])

    return (vector / np.math.factorial(4))[1:5]


def check_convex(game):
    is_convex = True

    all_coalision = [set(k.split(" ")) for k in game.keys() if k != "" and k != "1 2 3 4"]
    for s, t in itertools.combinations(all_coalision, 2):
        if not s & t:
            key_s = " ".join(sorted(list(s)))
            key_t = " ".join(sorted(list(t)))
            key_s_t = " ".join(sorted(list(s | t)))
            key_st = " ".join(sorted(list(s & t)))

            if game[key_st] + game[key_s_t] < game[key_s] + game[key_t]:
                is_convex = False

    return is_convex


def print_game(game):
    game_str = "; ".join(["v({{{0}}}) = {1}".format(k, v) for k, v in game.items()])
    print("Game:", game_str)


if __name__ == "__main__":
    variant_3 = {
        "": 0,
        "1": 3,
        "2": 4,
        "3": 1,
        "4": 2,
        "1 2": 7,
        "1 3": 5,
        "1 4": 6,
        "2 3": 5,
        "2 4": 7,
        "3 4": 3,
        "1 2 3": 10,
        "1 2 4": 10,
        "1 3 4": 9,
        "2 3 4": 9,
        "1 2 3 4": 12
    }
    while 1:
        is_super_additive, error_keys = check_super_additive(variant_3)
        print_game(variant_3)
        vector = get_vector_shepli(variant_3)
        print("Vector Sheply:", " ".join(["{0:.2f}".format(x) for x in vector]))
        print(int(vector.sum()), "=", variant_3["1 2 3 4"])
        for i in np.arange(1, 5):
            print("x{0}:".format(i), "{0:.2f}".format(vector[i-1]), ">=", variant_3[str(i)])

        print("Game of variant 3 is{0}super additive.".format(" " if is_super_additive else " not "))

        if is_super_additive:
            break
        print("Change game..")
        for key in set(error_keys):
            variant_3[key] += 1
        print()

    print("Game of variant 3 is{0}convex.".format(" " if check_convex(variant_3) else " not "))
