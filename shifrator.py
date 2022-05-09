# import math
# #s = input()
# #
# def fast_pow(x, y):
#     if y == 0:
#         return 1
#     if y == -1:
#         return 1. / x
#     p = fast_pow(x, y // 2)
#     p *= p
#     if y % 2:
#         p *= x
#     return p
# p = 99739967994999419933
# q = 39739967994999419933
# n = 3963663135943543412316970089006477724489
# h = 3963663135943543412177490153016478884624 # (p-1)*(q-1)
# d = 5
# e = 792732627188708682435498030603295776925
# l = list()
# desh = list()
# # for a in s:
# #     l.append(ord(a)-96)
# # #print(l)
# # for a in l:
# #     for i in range(e+1):
# #         a = a*a
# #         print(a)
# #     desh.append(a % n)
# # print(desh)
# print(fast_pow(2,10000000))
# -*- coding: 1251 -*-
import random
import time
import sys

# from numba import jit, njit
# import numpy as np
random.seed(1)
sys.setrecursionlimit(2500)


# @jit(nopython=True)
def binary(a, st, mod):
    ans = 1
    while st != 0:
        if st & 1 == 1:
            ans *= a
        a *= a
        if a > mod:
            a %= mod
        if ans > mod:
            ans %= mod

        st >>= 1
    return ans


precalc_N = 2 ** 2000


# @jit(nopython=True)
def extended(a, b):
    if a == 0:
        return b, 0, 1

    d, x1, y1 = extended(b % a, a)

    y = x1
    x = y1 - (b // a) * x1
    return d, x, y


# @jit(nopython=True)
def rabin_miller(n, r):
    b = n - 1
    k = -1
    b_i = []

    while True:
        k += 1
        b_i.append(b % 2)
        b //= 2
        if b <= 0:
            break

    for j in range(1, r + 1):
        a = random.randint(2, n - 1)
        d, _, _ = extended(a, n)
        if d > 1:
            return False

        for i in reversed(range(k + 1)):
            x = d
            d = (d * d) % n
            if d == 1 and x != 1 and x != n - 1:
                # print(1)
                return False

            if b_i[i] == 1:
                d = (d * a) % n
        if d != 1:
            return False
    return True


# @jit(nopython=True)
def is_prime(n):
    prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    for i in prime_numbers:
        if n % i == 0:
            if n == i:
                return True
            return False

    r = 20
    return rabin_miller(n, r)


# @jit(nopython=True)
def generate_prime(_n=precalc_N):
    while True:
        n = random.randint(2, _n)
        n = 2 * n - 1
        if is_prime(n):
            break
    return n


# @jit(nopython=True)
def generate_g(q_max, n_max):
    q = generate_prime(q_max)
    while True:
        # while True:
        n = random.randint(2, n_max - 1)
        if n % 2 != 0:
            n += 1
        p = n * q + 1
        if is_prime(p):
            break

    while True:
        a = random.randint(2, p - 2)
        g = binary(a, n, p)
        if g != 1:
            break

    return g, q, p


# @jit(nopython=True)
def diffie_hellman(g, x, q, p):
    x = x % q
    big_x = binary(g, x, p)
    return big_x


# @jit(nopython=True)
def encrypt(msg, key):
    return msg + key


# @jit(nopython=True)
def decrypt(msg, key):
    return msg - key


t = time.time()

g, q, p = generate_g(1 << 256, 1 << 2000)


while True:
    small_x = random.randint(2, p)
    big_x = diffie_hellman(g, small_x, q, p)
    if binary(big_x, q, p) == 1:
        break

while True:
    small_y = random.randint(2, p)
    big_y = diffie_hellman(g, small_y, q, p)
    if binary(big_y, q, p) == 1:
        break


key_a = binary(big_x, small_y, p)
key_b = binary(big_y, small_x, p)


assert key_a == key_b, 'not the same'
print('Key: ', key_a)

message_from_a = 321
message_from_b = 431



encrypted_message_from_a = encrypt(message_from_a, key_a)

decrypted_message_from_a = decrypt(encrypted_message_from_a, key_b)


encrypted_message_from_b = encrypt(message_from_b, key_a)

decrypted_message_from_b = decrypt(encrypted_message_from_b, key_b)

# print(decrypted_message_from_a, decrypted_message_from_b)

assert decrypted_message_from_b == message_from_b and decrypted_message_from_a == message_from_a, \
    "sms not the same"
print(time.time() - t)
#
# print(message_to_a_encrypted)