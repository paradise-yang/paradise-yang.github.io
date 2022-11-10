from email.contentmanager import raw_data_manager
import os
import random
import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.linalg import *

def openreadtxt(file_name, output_name):
    sigma_r = 5.0 # 旋转矩阵的噪声方差
    sigma_t = 0.1
    file = open(file_name,'r')  #打开文件
    file_data = file.readlines() #读取所有行
    output = open(output_name,'a')  #打开文件
    flag = 0
    for row in file_data:
        if (flag>=4) & (flag%2==0):
            row_list = row.split(' ') #按‘，’切分每行的数据
            position = map(float, [row_list[2], row_list[3], row_list[4], row_list[1]]) # scipy库的四元数顺序为 xyzw，colmap则为wzyx
            position = list(position) # 转float
            position = np.array(position) # 四元数
            r = R.from_quat(position)
            r_euler = r.as_euler('zyx', degrees=True)
            noise = np.random.normal(loc=0.0, scale=sigma_r, size=3)
            r_euler_noise = r_euler + noise
            r_euler = R.from_euler('zyx', r_euler_noise, degrees=True)
            r_quat = r_euler.as_quat()
            row_list[1] = str(r_quat[3]) # 赋值回去
            row = ' '.join(row_list)
            for i in range(2, 5):
                row_list[i] = str(r_quat[i-2])
                row = ' '.join(row_list)
            for k in range(5, 8):
                temp = float(row_list[k]) 
                noise = random.gauss(0, sigma_t) # 加噪声
                temp = temp + noise
                row_list[k] = str(temp)
                row = ' '.join(row_list)
            output.write(row)
            flag = flag + 1
        else:
            output.write(row)
            flag = flag + 1
    file.close()
    output.close()
    return flag
 
 
if __name__=="__main__":
    file_name = "/data/paradise/code/neddf/data/yzn-ori/text/images.txt"
    output_name = "/data/paradise/code/neddf/data/yzn-noise/text/images.txt"
    data = openreadtxt(file_name, output_name)