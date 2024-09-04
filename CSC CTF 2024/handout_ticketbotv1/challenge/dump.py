from ctypes import CDLL
from pickle import dump
from tqdm import tqdm
glibc = CDLL('./libc.so.6')
nums = {}
for i in tqdm(range(10000000)):
    glibc.srand(i)
    t = tuple(glibc.rand() for _ in range(3))   # 2 rand()s is statistically sufficient
  
    t = (t[1], t[2]) # remove the rand() that isn't printed by warmup
    nums[t] = nums.get(t, ())+(i,)
with open('srand_dict.pickle', 'wb') as f: dump(nums, f)