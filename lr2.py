import numpy as np


def generate_g(k):
    i_k = np.eye(k, dtype=int)
    x = np.array([[1, 1, 1],
                  [0, 1, 1],
                  [1, 0, 1],
                  [1, 1, 0]])
    g = np.hstack((i_k, x))
    return g


def generate_h(X, n, k):
    x_T = -X.T
    i_nk = np.eye(n - k, dtype=int)
    return np.hstack((x_T, i_nk))


def generate_syndromes(n, H):
    syndromes = {}
    for i in range(n):
        errors = np.zeros(n, dtype=int)
        errors[i] = 1
        syndrome = np.dot(H, errors) % 2
        syndromes[tuple(syndrome)] = errors
    return syndromes


def print_syndromes(S):
    for syndrome, position in S.items():
        syndrome_str = ''.join(map(str, syndrome))
        print(f"Синдром: [{syndrome_str}], Позиция ошибки: {position}")


def generate_v(G, U):
    return np.dot(U, G) % 2


def make_mistake_in_codeword(codeword):
    errors = np.zeros_like(codeword)
    errors[np.random.randint(0, n)] = 1
    return (codeword + errors) % 2


def make_two_mistakes_in_codeword(codeword, positions):
    errors = np.zeros_like(codeword)
    for p in positions:
        errors[p] = 1
    return (codeword + errors) % 2


def correct_mistake_in_codeword(mistaken_codeword, H, syndromes):
    syndrome = np.dot(H, mistaken_codeword) % 2
    syndrome_tuple = tuple(syndrome)

    if syndrome_tuple in syndromes:
        error_position = syndromes[syndrome_tuple]
        return (mistaken_codeword + error_position) % 2
    else:
        print("Синдром не найден в таблице")
        return mistaken_codeword


def generate_g_5(k):
    i_k = np.eye(k, dtype=int)
    x = np.array([
        [1, 1, 1, 0, 1],
        [0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 0]
    ])
    return np.hstack((i_k, x))


def generate_h_5(G_5):
    X = G_5[:, 5:]
    I_nk = np.eye(5, dtype=int)
    H_5 = np.hstack((X.T, I_nk))
    return H_5


def generate_syndromes(n, H):
    syndromes = {}
    for i in range(n):
        errors = np.zeros(n, dtype=int)
        errors[i] = 1
        syndrome = np.dot(H, errors) % 2
        syndromes[tuple(syndrome)] = errors
    return syndromes


def generate_syndromes_5(n, H):
    syndrome_table = {}

    for i in range(n):
        error_vector = np.zeros(n, dtype=int)
        error_vector[i] = 1
        syndrome = np.dot(H, error_vector) % 2
        syndrome_table[tuple(syndrome)] = error_vector

    for i in range(n):
        for j in range(i + 1, n):
            error_vector = np.zeros(n, dtype=int)
            error_vector[i] = 1
            error_vector[j] = 1
            syndrome = np.dot(H, error_vector) % 2
            syndrome_table[tuple(syndrome)] = error_vector

    return syndrome_table


if __name__ == "__main__":
    print("\nЧАСТЬ 1\n")
    k = 4  # Размерность кода (количество информационных символов)
    n = 7  # Общая длина кодового слова
    d = 3  # Минимальное расстояние
    U = np.array([1, 1, 1, 0])  # Информационное слово длины k = 4

    X = np.array([[1, 1, 1],
                  [0, 1, 1],
                  [1, 0, 1],
                  [1, 1, 0]])

    G = generate_g(k)  # Порождающая матрица
    H = generate_h(X, n, k)  # Проверочная матрица
    syndromes = generate_syndromes(n, H)  # Таблица синдромов
    print("2.1\nПорождающая матрица G:\n", G)
    print("\n2.2\nПроверочная матрица H:\n", H)
    print("\n2.3\nТаблица синдромов S:")
    print_syndromes(syndromes)

    codeword = generate_v(G, U)  # Кодовое слово V
    mistaken_codeword = make_mistake_in_codeword(codeword.copy())
    corrected_codeword = correct_mistake_in_codeword(mistaken_codeword, H, syndromes)
    print("\n2.4\nКодовое слово:", codeword)
    print("Кодовое слово с ошибкой:", mistaken_codeword)
    print("Исправленное слово:", corrected_codeword)

    codeword = generate_v(G, U)  # Кодовое слово V
    positions = np.random.choice(n, size=2, replace=False)
    twice_mistaken_codeword = make_two_mistakes_in_codeword(codeword.copy(), positions)
    corrected_codeword = correct_mistake_in_codeword(twice_mistaken_codeword, H, syndromes)
    print("\n2.5\nКодовое слово:", codeword)
    print("Кодовое слово с двумя ошибками:", twice_mistaken_codeword)
    print("Попытка исправления:", corrected_codeword)

    print("\nЧАСТЬ 2\n")
    k = 5  # Размерность кода (количество информационных символов)
    n = 10  # Общая длина кодового слова
    d = 5  # Минимальное расстояние
    G_5 = generate_g_5(k)  # Порождающая матрица
    H_5 = generate_h_5(G_5)  # Проверочная матрица
    syndromes_5 = generate_syndromes_5(n, H_5)  # Таблица синдромов
    print("2.6\nПорождающая матрица G_5:\n", G_5)
    print("\n2.7\nПроверочная матрица H_5:\n", H_5)
    print("\n2.8\nТаблица синдромов S_5:")
    print_syndromes(syndromes_5)

    U_5 = np.array([1, 0, 1, 1, 0])
    codeword_5 = generate_v(G_5, U_5)  # Кодовое слово V_5
    mistaken_codeword_5 = make_mistake_in_codeword(codeword_5.copy())
    corrected_codeword_5 = correct_mistake_in_codeword(mistaken_codeword_5, H_5, syndromes_5)
    print("\n2.9\nКодовое слово:", codeword_5)
    print("Кодовое слово с ошибкой:", mistaken_codeword_5)
    print("Исправленное слово:", corrected_codeword_5)

    positions = np.random.choice(n, size=2, replace=False)
    twice_mistaken_codeword_5 = make_two_mistakes_in_codeword(codeword_5.copy(), positions)
    corrected_codeword_5 = correct_mistake_in_codeword(twice_mistaken_codeword_5, H_5, syndromes_5)
    print("\n2.10\nКодовое слово:", codeword_5)
    print("Кодовое слово с двумя ошибками:", twice_mistaken_codeword_5)
    print("Исправленное слово:", corrected_codeword_5)

    positions = np.random.choice(n, size=3, replace=False)
    thrice_mistaken_codeword_5 = make_two_mistakes_in_codeword(codeword_5.copy(), positions)
    corrected_codeword_5 = correct_mistake_in_codeword(thrice_mistaken_codeword_5, H_5, syndromes_5)
    print("\n2.11\nКодовое слово:", codeword_5)
    print("Кодовое слово с тремя ошибками:", thrice_mistaken_codeword_5)
    print("Попытка исправления:", corrected_codeword_5)
