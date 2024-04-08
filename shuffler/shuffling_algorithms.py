import numpy as np
import random
import heapq


def random_shuffle(index_array):
    n = len(index_array)
    for i in range(n):
        j = random.randint(0, n-1)
        index_array[i], index_array[j] = index_array[j], index_array[i]
    return index_array

def fisher_yates_shuffle(index_array):
    for i in range(len(index_array) - 1, 0, -1):
        j = random.randint(0, i)
        index_array[i], index_array[j] = index_array[j], index_array[i]
    return index_array

def poisson_charlier_shuffle(index_array: np.array, alpha=0.5, lam=10):
    def poisson_charlier(alpha, lam, size):
        assert alpha >= -1, "Alpha should be greater than or equal to -1."
        Y = np.random.poisson(lam=lam, size=size)
        X = Y + np.random.binomial(n=Y, p=alpha / (1 + alpha))
        return X

    size = index_array.size
    pc_distribution = poisson_charlier(alpha, lam, size)
    shuffled_indices = np.argsort(pc_distribution)
    index_array = index_array[shuffled_indices]
    return index_array

def boriga_dascalescu_shuffle(index_array):
    n = len(index_array)
    L = [0] * n 
    q = [0] * n 

    max_val = n
    for i in range(n):
        q[i] = random.randint(0, n-1)
        while L[q[i]] == 1:
            k = max_val - 1
            while L[k] == 1:
                k -= 1
            q[i] = k
            max_val = k

        L[q[i]] = 1
    return q

def boriga_dascalescu_shuffle_set(index_array):
    n = len(index_array)

    unused = set([*range(n)])
    used = set()

    result = []

    for _ in range(n):
        # generam un indice aleatoriu
        value = random.randint(0, n-1)

        # daca indicele generat a fost deja utilizat
        if value in used:
            # extragem indicele minim neutilizat din min-heao
            value = unused.pop()
        else:
            # daca indicele generat  nu a fost deja utilizat, atunci il folosim acum
            unused.remove(value)

        # marcam indicele utilizat
        used.add(value)
        result.append(value)

    return result

def boriga_dascalescu_shuffle_heap(index_array):
    n = len(index_array)
    L = [0] * n
    q = [*range(n)] 
    heapq._heapify_max(q)
    # heapq.heapify(q) # similar performance in terms of time efficiency
    result = []
    for _ in range(n):
        selected = random.randint(0, n-1)
        while L[selected] == 1:
            selected = heapq.heappop(q)
        L[selected] = 1
        result.append(selected)
    return result

def boriga_dascalescu_shuffle_heap2(index_array):
    n = len(index_array)
    L = [0] * n
    q = [*range(n)] 
    heapq._heapify_max(q)
    # heapq.heapify(q) # similar performance in terms of time efficiency
    result = []
    for _ in range(n):
        selected = random.randint(0, n-1)
        if L[selected] == 1:
            selected = heapq.heappop(q)
        else:
            q.remove(selected)
            heapq._heapify_max(q)
        L[selected] = 1
        result.append(selected)
    return result

