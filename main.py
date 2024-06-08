from analysis import *
import random
bits=[]
times=[]
print("请输入需要取得的随机数的最大值")
n=int(input())
nums=[random.randint(0,n-1)for i in range(500000)]
print(nums)
for i in range(n):
    times.append(0)
    #给次数初始置0
for i in nums:
    times[i]=times[i]+1
print("出现次数按顺序为：",times)

intervals=[]
interval=[]
for i in range(n*n):
    interval.append(0)
    #给次数初始置0
for i in range(n):
    intervals.append(interval)
    #构造二维数组
for i in nums:
    for j in range(n):
        if j==i:
            intervals[i][intervals[i][0]]+=1
            intervals[i][0]=0
        else:
            intervals[j][0]+=1
for i in range(n):
    print(f"{i}在随机数中出现的间隔分布情况为：")
    for j in range(n * n):
        if j==0:continue
        if intervals[i][j]!=0: print(f"间隔{j-1}个数出现的次数为{intervals[i][j]}")
    print("")
m=1 #选取用于计算二进制形式的除数
while 2*m<n:
    m=m*2
m=m/2

for a in nums:
    if a>=2*m: continue
    k=m
    while k!=0.5:
        bits.append(int(a//k))
        a=a%k
        k=k/2
#将n的数以二进制每位进入bits列表

import pickle
file=open('mylist_pkl.txt','w')
for i in bits:
    file.write(str(i))
file.close()

print("monobit test:")
p=monobit_test(bits)
print("p=",p)
print("")

print("frequency within block test:")
p=frequency_within_block_test(bits)
print("p=",p)
print("")

print("cumulative sums test:")
plist=cumulative_sums_test(bits)
print("plist=",plist)
print("")

print( "run test:")
p=runs_test(bits)
print("p=",p)
print("")

print("longest run ones in a block test:")
p = longest_run_ones_in_a_block_test(bits)
print("p=", p)
print("")

print("approximate entropy test:")
p = approximate_entropy_test(bits)
print("p=", p)
print("")

import math
import matplotlib.pyplot as plt
#梅森旋转算法生成均匀分布
class MersenneTwister:
    def __init__(self, seed):
        # seed的范围为-2147483648到2147483647
        self.index = 624  # 初始化索引
        self.mt = [0] * 624  # 初始化状态数组
        self.mt[0] = seed  # 使用种子初始化状态数组的第一个元素
        for i in range(1, 624):  # 初始化状态数组的其余元素
            self.mt[i] = 0xFFFFFFFF & (1812433253 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i)

    def extract_number(self):
        if self.index >= 624:  # 如果索引超出范围，进行扭曲操作
            self.twist()

        y = self.mt[self.index]  # 取出状态数组中的一个元素
        y = y ^ (y >> 11)  # 对取出的元素进行位运算
        y = y ^ ((y << 7) & 0x9D2C5680)  # 对取出的元素进行位运算
        y = y ^ ((y << 15) & 0xEFC60000)  # 对取出的元素进行位运算
        y = y ^ (y >> 18)  # 对取出的元素进行位运算

        self.index += 1  # 更新索引
        return 0xFFFFFFFF & y  # 返回生成的随机数
    def random(self):
        # 返回0-1的随机数
        return self.extract_number() / 0xFFFFFFFF

    def twist(self):
        for i in range(624):  # 扭曲操作
            y = (self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff)
            self.mt[i] = self.mt[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908B0DF
        self.index = 0  # 重置索引
def count(lst,max_value,d):
    # 统计lst中每个范围内数值的出现次数,d为组距
    result=[0]*math.ceil(max_value/d) # ceil为向上取整
    for i in lst:
        result[int(i//d)]+=1
    return result

seed = random.randint(-10000,10000)  # 设置随机数种子
mt = MersenneTwister(seed)
lst=[];cnt=10000
for i in range(cnt):
    lst.append(mt.random()*n)
print(lst)
lst=count(lst,n,0.01)
plt.bar(range(len(lst)),lst)
plt.title("uniform distribution")
plt.show()

import numpy as np
label = "Gaussian distribution"
np.random.normal
fig = plt.figure()
ax = fig.add_subplot(1,2,1)
gauss=[]
for i in range(10000):
    gauss.append(np.random.normal(0,1))
print(gauss)
ax.set_title(label)
plt.hist(gauss,100)
plt.show()

