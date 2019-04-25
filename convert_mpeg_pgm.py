from PIL import Image
import numpy as np
import os
import os.path as osp

def to_string(x):
	return [str(i) for i in x]

def check_binary(x):
	for pixel in x:
		if pixel != "0" and pixel != "1":
			print("ERROR")
			return

def convert_numpy_str(x):
	str_x = to_string(x)
	check_binary(str_x)
	ans = " ".join(str_x)
	return ans

def convert_image_pgm(img, file_path):
	img = np.array(img)
	img = img // np.max(img)
	file = open(file_path, "w")
	file.write("P2\n")
	file.write("{} {}\n".format(img.shape[1], img.shape[0]))
	file.write("1\n")
	for l in img:
		file.write(convert_numpy_str(l)+" \n")
	file.close()

if __name__ == '__main__':
	file_names = os.listdir("mpeg7/")
	for file_name in file_names:
		img = Image.open(osp.join("mpeg7/", file_name))
		print("Converting ", file_name)
		out_file_name = file_name[:-3] + "pgm"
		out_dir = osp.join("MO445-descriptors/examples/mpeg7_pgm/", out_file_name)
		convert_image_pgm(img, out_dir)

