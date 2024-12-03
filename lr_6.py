import numpy as np
import random


def polynomial_division_remainder(dividend, divisor):
    remainder = np.array(dividend, dtype=int)
    len_divisor = len(divisor)

    for i in range(len(remainder) - len_divisor + 1):
        if remainder[i] != 0:
            remainder[i:i + len_divisor] ^= divisor

    return remainder[-(len_divisor - 1):]


def polynomial_multiply(A, B):
    result = np.zeros(len(A) + len(B) - 1, dtype=int)
    for i in range(len(A)):
        result[i:i + len(B)] ^= A[i] * B
    return result


def introduce_and_fix_error(a, g, error_rate):
    print("Входное сообщение:      ", a)
    print("Порождающий полином:    ", g)

    v = polynomial_multiply(a, g)
    print("Отправленное сообщение: ", v)

    w = v.copy()
    error = np.zeros(len(w), dtype=int)
    error_indices = random.sample(range(len(w)), error_rate)
    error[error_indices] = 1

    w = (w + error) % 2
    print("Сообщение с ошибкой:    ", w)

    s = polynomial_division_remainder(w, g)

    if len(g) == 4:
        for i in range(len(w)):
            e = np.zeros(len(w), dtype=int)
            e[i] = 1
            if np.array_equal(polynomial_division_remainder(e, g), s):
                w[i] ^= 1
                break
    else:
        for i in range(len(w)):
            e = np.zeros(len(w), dtype=int)
            e[i] = 1
            if np.array_equal(polynomial_division_remainder(e, g), s):
                w[i] ^= 1
                break

        if np.array_equal(polynomial_division_remainder(w, g), np.zeros(len(g) - 1, dtype=int)) == False:
            for i in range(len(w)):
                for j in range(i + 1, len(w)):
                    e = np.zeros(len(w), dtype=int)
                    e[i] = 1
                    e[j] = 1
                    if np.array_equal(polynomial_division_remainder(e, g), s):
                        w[i] ^= 1
                        w[j] ^= 1
                        break
                if np.array_equal(polynomial_division_remainder(w, g), np.zeros(len(g) - 1, dtype=int)):
                    break

    print("Исправленное сообщение: ", w)

    if np.array_equal(v, w):
        print("Ошибка исправлена корректно")
    else:
        print("Ошибка исправлена некорректно")
    print()

a = np.array([1, 0, 0, 1])
g = np.array([1, 0, 1, 1])
introduce_and_fix_error(a, g, 1)
introduce_and_fix_error(a, g, 2)
introduce_and_fix_error(a, g, 3)
a_2 = np.array([1, 0, 0, 1, 0, 0, 0, 1, 1])
g_2 = np.array([1, 0, 0, 1, 1, 1, 1])
introduce_and_fix_error(a_2, g_2, 1)
introduce_and_fix_error(a_2, g_2, 2)
introduce_and_fix_error(a_2, g_2, 3)