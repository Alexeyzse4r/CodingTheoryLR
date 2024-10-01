import numpy as np
from itertools import combinations

A = [
[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
[0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
[0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
[1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
[0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0],
[1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
]

# A = [[ 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
# [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
# [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
# [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]]

# A = [[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
# [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
# [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
# [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1],
# [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0],
# [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]]

A = np.array(A)
def REF(M):
    res_M = []
    for i in range(len(M[0])):
        for j in range(len(M)):
            if M[j][i] != 0:
                res_M.append(M[j])
                M = np.delete(M, j, axis=0)
                break
    return res_M


def RREF(M):
    M=REF(M)
    num_zero_mass=[]
    for now_str in M:
        num_zero=0
        for i in range(len(now_str)):
            if now_str[i]==0:
                num_zero+=1
            else:
                break
        num_zero_mass.append(num_zero)

    for i in range(1, len(M)):
        for j in range(i):
            if M[j][num_zero_mass[i]] > 0:
                M[j] -= M[i]
            elif M[j][num_zero_mass[i]] < 0:
                M[j] += M[i]

    return M


def task_1_3_and_1_4(M):
    # 1.3.1
    for i in range(len(M)):
        max_row = np.argmax(np.abs(M[i:len(M), i])) + i
        M[[i, max_row]] = M[[max_row, i]]

        if M[i, i] == 0:
            continue
        M[i] = M[i] / M[i, i]

        for j in range(i + 1, len(M)):
            M[j] = M[j] - M[j, i] * M[i]

    for i in M:
        for j in i:
            print(j, '\t', end='')
        print('\n')
    print('---------------------------')
    #1.3.2
    print('n = ', M.shape[0], '\nk = ', M.shape[1])
    #1.3.3
    #step1
    M = np.delete(M, j, axis=0)
    G = M.copy()
    lead = 0
    for r in range(len(M)):
        if lead >= len(M[0]):
            return M
        i = r
        while M[i][lead] == 0:
            i += 1
            if i == len(M):
                i = r
                lead += 1
                if len(M[0]) == lead:
                    return M
        M[[i, r]] = M[[r, i]]
        M[r] = M[r] / M[r][lead]
        for i in range(len(M)):
            if i != r:
                M[i] = M[i] - M[i][lead] * M[r]
        lead += 1
    for i in M:
        for j in i:
            print(j, '\t', end='')
        print('\n')
    print('---------------------------')

    #step2
    lead = []
    for j in M:
        for i in range(len(j)):
            if j[i] != 0:
                lead.append(i)
                break
    print(lead)
    #step3
    for i, lead_zn in enumerate(lead):
        M = np.delete(M, lead_zn-i, axis=1)
    for i in M:
        for j in i:
            print(j, '\t', end='')
        print('\n')
    print('---------------------------')
    #step4
    I = np.zeros(shape=(len(M[0]), len(M[0])), dtype=int)
    for i in range(len(I)):
        I[i][i]=1
    temp_iter_for_I = 0
    temp_iter_for_M = 0
    H = []
    for i in range(lead[len(lead)-1]+1):
        if i == lead[temp_iter_for_M]:
            H.append(M[temp_iter_for_M])
            temp_iter_for_M += 1
        else:
            H.append(I[temp_iter_for_I])
            temp_iter_for_I += 1

    for i in range(temp_iter_for_I, len(I)):
        H.append(I[i])
    for i in H:
        for j in i:
            print(j, '\t', end='')
        print('\n')
    print('---------------------------')





    # 1.4.1
    def check_by_H(codeword, H):
        return np.dot(codeword, H) % 2

    codewords = set()
    for r in range(1, len(G) + 1):
        for comb in combinations(range(len(G)), r):
            codeword = np.bitwise_xor.reduce(G[list(comb)], axis=0)
            codewords.add(tuple(codeword))
    codewords.add(tuple(np.zeros(G.shape[1], dtype=int)))
    codewords = np.array(list(codewords))
    print(codewords) #все кодовые слова 1 способом
    print('---------------------------')

    for i in range(len(codewords)):
        temp_mass = check_by_H(codewords[i], H)
        temp_flag_error = False
        for j in range(len(temp_mass)):
            if temp_mass[j] != 0:
                temp_flag_error = True
                print('Слово', codewords[i], ' не прошло проверку')

    min_d = float('inf')
    for i in range(len(codewords)):
        for j in range(i + 1, len(codewords)):
            distance = np.sum(np.bitwise_xor(codewords[i], codewords[j]))
            if distance > 0:
                min_d = min(min_d, distance)
    print('Кодовое расстояние > ', min_d)




    # 1.4.2
    n = len(G)
    codewords = []
    for i in range(2**n):
        binary_word = np.array(list(np.binary_repr(i, n)), dtype = int)
        codeword = np.dot(binary_word, G) % 2
        codewords.append(codeword)
    codewords = np.array(codewords)
    print(codewords)#все кодовые слова 2 способом
    print('---------------------------')


    for i in range(len(codewords)):
        temp_mass = check_by_H(codewords[i], H)
        temp_flag_error = False
        for j in range(len(temp_mass)):
            if temp_mass[j] != 0:
                temp_flag_error = True
                print('Слово', codewords[i], ' не прошло проверку')

    min_d = float('inf')
    for i in range(len(codewords)):
        for j in range(i + 1, len(codewords)):
            distance = np.sum(np.bitwise_xor(codewords[i], codewords[j]))
            if distance > 0:
                min_d = min(min_d, distance)
    print('Кодовое расстояние > ', min_d)




# 1.1
# new_A = REF(A)

# 1.2
# new_A = RREF(A)

# 1.3, 1.4
new_A = task_1_3_and_1_4(A)

