import math

from fractions import Fraction
from gammafunction import *

import numpy
import cmath
import random
import copy
#选取了六种测评方式实现：单比特测试，块内频率测试，累积和测试，游程测试，块内长程1测试，近似熵测试
def count_ones_zeroes(bits):
    #数一共有多少个0和1
    ones = 0
    zeroes = 0
    for bit in bits:
        if (bit == 1):
            ones += 1
        else:
            zeroes += 1
    return (zeroes, ones)


def monobit_test(bits):
    n = len(bits)

    zeroes, ones = count_ones_zeroes(bits)
    s = abs(ones - zeroes)
    print("  Ones count   = %d" % ones)
    print("  Zeroes count = %d" % zeroes)

    p = math.erfc(float(s) / (math.sqrt(float(n)) * math.sqrt(2.0)))

    success = (p >= 0.01)
    if success:
        print("monobit test PASS")
    else:
        print("monobit test FAIL: Data not random")
    return (p)


def frequency_within_block_test(bits):
    # M为块的大小，N为块的个数
    # N = floor(n/M)
    # M的值在20到100之间
    n = len(bits)
    M = 20
    N = int(math.floor(n / M))
    if N > 99:
        N = 99
        M = int(math.floor(n / N))

    if len(bits) < 100:
        print("Too little data for test. Supply at least 100 bits")
        return(0)

    print("  n = %d" % len(bits))
    print("  N = %d" % N)
    print("  M = %d" % M)

    num_of_blocks = N
    block_size = M
    #后面为有关函数的数学计算
    proportions = list()
    for i in range(num_of_blocks):
        block = bits[i * (block_size):((i + 1) * (block_size))]
        zeroes, ones = count_ones_zeroes(block)
        proportions.append(Fraction(ones, block_size))

    chisq = 0.0
    for prop in proportions:
        chisq += 4.0 * block_size * ((prop - Fraction(1, 2)) ** 2)

    p = gammaincc((num_of_blocks / 2.0), float(chisq) / 2.0)
    success = (p >= 0.01)
    if success:
        print("frequency within block test PASS")
    else:
        print("frequency within block test FAIL: Data not random")
    return (p)



def normcdf(n):
    return 0.5 * math.erfc(-n * math.sqrt(0.5))


def p_value(n, z):
    sum_a = 0.0
    startk = int(math.floor((((float(-n) / z) + 1.0) / 4.0)))
    endk = int(math.floor((((float(n) / z) - 1.0) / 4.0)))
    for k in range(startk, endk + 1):
        c = (((4.0 * k) + 1.0) * z) / math.sqrt(n)
        d = normcdf(c)
        c = (((4.0 * k) - 1.0) * z) / math.sqrt(n)
        e = normcdf(c)
        sum_a = sum_a + d - e

    sum_b = 0.0
    startk = int(math.floor((((float(-n) / z) - 3.0) / 4.0)))
    endk = int(math.floor((((float(n) / z) - 1.0) / 4.0)))
    for k in range(startk, endk + 1):
        c = (((4.0 * k) + 3.0) * z) / math.sqrt(n)
        d = normcdf(c)
        c = (((4.0 * k) + 1.0) * z) / math.sqrt(n)
        e = normcdf(c)
        sum_b = sum_b + d - e

    p = 1.0 - sum_a + sum_b
    return p


def cumulative_sums_test(bits):
    n = len(bits)
    # Step 1 : 将01序列变为 1与-1的序列
    x = list()
    for bit in bits:
        x.append((bit * 2) - 1)

    # Steps 2 计算Si
    # Compute the partial sum and records the largest excursion.
    pos = 0
    forward_max = 0
    for e in x:
        pos = pos + e
        if abs(pos) > forward_max:
            forward_max = abs(pos)
    pos = 0
    backward_max = 0
    for e in reversed(x):
        pos = pos + e
        if abs(pos) > backward_max:
            backward_max = abs(pos)

    # Step 3 得出 p_value
    p_forward = p_value(n, forward_max)
    p_backward = p_value(n, backward_max)

    success = ((p_forward >= 0.01) and (p_backward >= 0.01))
    plist = [p_forward, p_backward]

    if success:
        print("cumulative sums test PASS")
    else:
        print("cumulative sums test FAIL: Data not random")
    return (plist)





def runs_test(bits):
    n = len(bits)
    zeroes, ones = count_ones_zeroes(bits)

    prop = float(ones) / float(n)
    print("  prop ", prop)

    tau = 2.0 / math.sqrt(n)
    print("  tau ", tau)

    if abs(prop - 0.5) > tau:
        return (False, 0.0, None)

    vobs = 1.0
    for i in range(n - 1):
        if bits[i] != bits[i + 1]:
            vobs += 1.0

    print("  vobs ", vobs)

    p = math.erfc(abs(vobs - (2.0 * n * prop * (1.0 - prop))) / (2.0 * math.sqrt(2.0 * n) * prop * (1 - prop)))
    success = (p >= 0.01)
    if success:
        print("runs test PASS")
    else:
        print("runs test FAIL: Data not random")
    return (p)



def probs(K, M, i):
    M8 = [0.2148, 0.3672, 0.2305, 0.1875]
    M128 = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    M512 = [0.1170, 0.2460, 0.2523, 0.1755, 0.1027, 0.1124]
    M1000 = [0.1307, 0.2437, 0.2452, 0.1714, 0.1002, 0.1088]
    M10000 = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
    if (M == 8):
        return M8[i]
    elif (M == 128):
        return M128[i]
    elif (M == 512):
        return M512[i]
    elif (M == 1000):
        return M1000[i]
    else:
        return M10000[i]


def longest_run_ones_in_a_block_test(bits):
    n = len(bits)

    if n < 128:
        print("the numbers are too few")
        return (0)
    elif n < 6272:
        M = 8
    elif n < 750000:
        M = 128
    else:
        M = 10000

    # 根据输入的数量计算不同的K和N
    if M == 8:
        K = 3
        N = 16
    elif M == 128:
        K = 5
        N = 49
    else:
        K = 6
        N = 75

    #  记录频率
    v = [0, 0, 0, 0, 0, 0, 0]

    for i in range(N):
        # 找到最长游程
        block = bits[i * M:((i + 1) * M)]  # 第i个分块

        run = 0
        longest = 0
        for j in range(M):  # 数比特数
            if block[j] == 1:
                run += 1
                if run > longest:
                    longest = run
            else:
                run = 0

        if M == 8:
            if longest <= 1:
                v[0] += 1
            elif longest == 2:
                v[1] += 1
            elif longest == 3:
                v[2] += 1
            else:
                v[3] += 1
        elif M == 128:
            if longest <= 4:
                v[0] += 1
            elif longest == 5:
                v[1] += 1
            elif longest == 6:
                v[2] += 1
            elif longest == 7:
                v[3] += 1
            elif longest == 8:
                v[4] += 1
            else:
                v[5] += 1
        else:
            if longest <= 10:
                v[0] += 1
            elif longest == 11:
                v[1] += 1
            elif longest == 12:
                v[2] += 1
            elif longest == 13:
                v[3] += 1
            elif longest == 14:
                v[4] += 1
            elif longest == 15:
                v[5] += 1
            else:
                v[6] += 1

    # 计算chi_sq
    chi_sq = 0.0
    for i in range(K + 1):
        p_i = probs(K, M, i)
        upper = (v[i] - N * p_i) ** 2
        lower = N * p_i
        chi_sq += upper / lower
    print("  n = " + str(n))
    print("  K = " + str(K))
    print("  M = " + str(M))
    print("  N = " + str(N))
    print("  chi_sq = " + str(chi_sq))
    p = gammaincc(K / 2.0, chi_sq / 2.0)

    success = (p >= 0.01)
    if success:
        print("longest run ones in a block test PASS")
    else:
        print("longest run ones in a block test FAIL: Data not random")
    return (p)




def bits_to_int(bits):
    theint = 0
    for i in range(len(bits)):
        theint = (theint << 1) + bits[i]
    return theint


def approximate_entropy_test(bits):
    n = len(bits)

    m = int(math.floor(math.log(n, 2))) - 6
    if m < 2:
        m = 2
    if m > 3:
        m = 3

    print("  n         = ", n)
    print("  m         = ", m)

    Cmi = list()
    phi_m = list()
    for iterm in range(m, m + 2):
        # Step 1
        padded_bits = bits + bits[0:iterm - 1]

        # Step 2
        counts = list()
        for i in range(2 ** iterm):
            count = 0
            for j in range(n):
                if bits_to_int(padded_bits[j:j + iterm]) == i:
                    count += 1
            counts.append(count)
            print("  Pattern %d of %d, count = %d" % (i + 1, 2 ** iterm, count))

        # step 3
        Ci = list()
        for i in range(2 ** iterm):
            Ci.append(float(counts[i]) / float(n))

        Cmi.append(Ci)

        # Step 4
        sum = 0.0
        for i in range(2 ** iterm):
            if (Ci[i] > 0.0):
                sum += Ci[i] * math.log((Ci[i] / 10.0))
        phi_m.append(sum)
        print("  phi(%d)    = %f" % (m, sum))

    # Step 5 完成前四步的循环

    # Step 6
    appen_m = phi_m[0] - phi_m[1]
    print("  AppEn(%d)  = %f" % (m, appen_m))
    chisq = 2 * n * (math.log(2) - appen_m)
    print("  ChiSquare = ", chisq)
    # Step 7
    p = gammaincc(2 ** (m - 1), (chisq / 2.0))

    success = (p >= 0.01)
    if success:
        print("approximate entropy test PASS")
    else:
        print("approximate entropy test FAIL: Data not random")
    return (p)


