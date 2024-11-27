import os
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
import shutil
import csv
import pandas as pd

# 源文件夹和目标文件夹路径
folder_path = '5w_fits'  # 文件夹路径
target_fits_folder = 'ex_fits'
'''
if not os.path.exists(target_fits_folder):
    os.makedirs(target_fits_folder)
naxis2_list = []
# flux_list = np.zeros((2000,3600))
i = 0
minwave = []
maxwave = []
ex_filenames = []
# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
  if filename.endswith('.fits'):
        file_path = os.path.join(folder_path, filename)
        try:
            with fits.open(file_path) as hdul:
                hdu1_data = hdul[1].data
                loglam = hdu1_data['loglam']
                flux = hdu1_data['flux']
                #flux_list[i] = flux
                #i = i+1
                #print(flux)
                
                # 转换为实际波长
                wavelengths = 10 ** loglam
                sta = wavelengths[0]
                end = wavelengths[-1]
                minwave.append(sta)
                maxwave.append(end)
                # 波长范围 提取起始值大于3830 结束值小于8000的光谱文件名（共43个）
                if sta > 3830:
                    ex_filenames.append(filename)
                if end < 8000:
                    ex_filenames.append(filename)
                hdu1_header = hdul[1].header
                naxis1 = hdu1_header['NAXIS1']
                naxis2 = hdu1_header['NAXIS2']
                naxis2_list.append(naxis2)
		 #print(f"文件名: {filename}")
		 #print(f"波长: {wavelengths}")
		#print(f"数据维度（NAXIS1 x NAXIS2）: {naxis1} x {naxis2}")

	    #print("-" * 20)
	# 如果出现异常，打印错误信息并跳过当前文件
        except Exception as e:
            ex_filenames.append(filename)
            print(f"Error reading file {filename}: {e}")
            continue  # 跳过当前文件，继续处理下一个文件
print(f"剔除光谱数量:{len(ex_filenames)}")

# 定义文件名
file_name = "ex_fitsnames.txt"

# 使用'w'模式打开文件，如果文件不存在则创建
with open(file_name, 'w') as file:
    # 遍历数组中的每个元素
    for item in ex_filenames:
        # 写入元素到文件，并在每个元素后面添加换行符
        file.write(item + '\n')

print(f"数组内容已写入到 {file_name}")

print(f"剔除光谱数量:{len(ex_filenames)}")

# 遍历文件名列表
for file_name in ex_filenames:
    source_path = os.path.join(folder_path, file_name)
    target_path = os.path.join(target_fits_folder, file_name)
    # 检查源文件是否存在
    if not os.path.exists(source_path):
        print(f"文件 {source_path} 不存在，跳过剪切。")
        continue  # 跳过剪切，继续下一个文件
    shutil.move(source_path, target_path)

print("文件剪切完成")
'''


txt_file_path = 'ex_fitsnames.txt'  

array2 = []  # 存储txt文件中的文件名
# 读取txt文件，并将文件名写入数组2
with open(txt_file_path, 'r') as file:
    for line in file:
        array2.append(line.strip())  # 使用strip()去除可能的换行符

'''
# 编写插值函数
def inter_wave(fits_name):
    hdu_list = fits.open(fits_name)
    t = hdu_list[1].data
    flux = t['flux']
    wave1 = t['loglam']
    wave = 10 ** wave1

    # 剪切波长数组和相应的纵坐标数组
    cut_wavelength = wave[(wave >= 3829) & (wave <= 8001)]
    cut_flux = flux[(wave >= 3829) & (wave <= 8001)]

    # 创建插值函数，将波长取整，并进行插值
    interp_func = interp1d(cut_wavelength, cut_flux, kind='linear')
    new_wavelength = np.arange(np.ceil(cut_wavelength[0]), np.floor(cut_wavelength[-1]) + 1, 1)
    new_flux = interp_func(new_wavelength)
    return new_flux

# 遍历文件夹中的fits文件，将所有的光谱文件进行处理
# 存储所有文件的处理结果的大数组
all_data = []
files = []
# 遍历文件夹中的文件

for file_name in os.listdir(folder_path):
    # 构建文件的完整路径
    file_path = os.path.join(folder_path, file_name)
    files.append(file_name)
    # 调用inter_wave函数处理单个文件，并将返回的数组添加到大数组中
    data = inter_wave(file_path)
    all_data.append(data)

# 将大数组转换为NumPy数组
all_data = np.array(all_data)

# 输出大数组的形状
print(all_data.shape)

# 读取CSV文件
df = pd.read_csv("5w_data.csv")

# 创建空列表用于存储图像名、年龄和金属丰度
images_names_list = []
logAge_list = []
MH_list = []


for name in files:
    # 在CSV文件中查找对应的姓名
    row = df.loc[df["fitsname"] == name]
    # 提取图像名、年龄和金属丰度
    images_names = row["photo_name"].values[0]
    logAges = row["logAge"].values[0]
    MHs = row["MH"].values[0]

    images_names_list.append(images_names)
    logAge_list.append(logAges)
    MH_list.append(MHs)


# 准备写入CSV的数据
data_to_write = []
# 列标题
headers = ["photo_name", "fits_name"] + [f"{col}" for col in range(3830, 8001)] + ["logAge", "MH"]
# 遍历列表和数组的长度
for i in range(len(files)):
    row = [images_names_list[i], files[i]] + list(all_data[i, :])
    row.extend([logAge_list[i], MH_list[i]])
    # 将合并后的行添加到数据列表中
    data_to_write.append(row)

# 定义CSV文件名
csv_filename = 'pre_data.csv'

# 打开文件用于写入，并使用csv.writer写入数据
with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # 写入列标题
    csvwriter.writerow(headers)

    # 写入数据到CSV文件
    for row in data_to_write:
        csvwriter.writerow(row)

print(f'数据已写入CSV文件：{csv_filename}')
'''
# 根据不符合要求的光谱文件名找到对应的图像名
# 读取CSV文件
df = pd.read_csv("5w_data.csv")

# 创建空列表用于存储图像名、年龄和金属丰度
ex_images_names = []

# 遍历列表中的姓名
for name in array2:
    # 在CSV文件中查找对应的姓名
    row = df.loc[df["fitsname"] == name]
    # 提取图像名、年龄和金属丰度
    ex_images = row["photo_name"].values[0]

    ex_images_names.append(ex_images)

print(f'对应图像数量：{len(ex_images_names)}')

# 源文件夹和目标文件夹路径
source_image_folder = '5w_images'
target_folder = 'ex_images'
if not os.path.exists(target_folder):
    os.makedirs(target_folder)
# 遍历文件名列表
for file_name in ex_images_names:
    source_path = os.path.join(source_image_folder, file_name)
    target_path = os.path.join(target_folder, file_name)
    # 检查源文件是否存在
    if not os.path.exists(source_path):
        print(f"文件 {source_path} 不存在，跳过剪切。")
        continue  # 跳过剪切，继续下一个文件
    shutil.move(source_path, target_path)

print("文件剪切完成")


