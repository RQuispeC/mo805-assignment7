import os
import os.path as osp
import numpy as np

base = "mpeg7_pgm/"
files_names = os.listdir(base)
files_names.sort()
f = open("names.txt", "w")
for l in files_names:
	f.write(l[:-4]+ '\n')
f.close()

f2 = open("paths.txt", "w")
for l in files_names:
	f2.write(osp.join(base, l)+ '\n')
f2.close()
