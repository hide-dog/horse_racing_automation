import os
import re

a = [str(2021-num) for num in range(20)]
b = [str(num+1).zfill(2) for num in range(10)]

for i in a:
    for j in b:
        path = i + "_data/" + j
        os.makedirs(path, exist_ok=True)
    #end
#end
