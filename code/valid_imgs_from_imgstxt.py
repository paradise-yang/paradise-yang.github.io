from email.contentmanager import raw_data_manager
import os
import shutil
from scipy.spatial.transform import Rotation as R
from scipy.linalg import *

def valid_imgs(file_name, input_path, output_path):
    file = open(file_name,'r')  #打开文件
    file_data = file.readlines() #读取所有行
    items = []
    flag = 0
    for row in file_data:
        if (flag>=4) & (flag%2==0):
            row_list = row.split(' ') #按‘，’切分每行的数据
            item = row_list[9][:-1]
            image = os.path.join(input_path, item)
            shutil.copy(image, output_path)
            items.append(item)
        flag = flag + 1
    # print(items)
    print(len(items))
        

if __name__=="__main__":
    file_name = "C:/Users/paradise/Desktop/up/text/images.txt" # images.txt 文件
    input_path = "C:/Users/paradise/Desktop/up/mask/" # 原始图片路径
    output_path = "C:/Users/paradise/Desktop/up/new_mask/" # 提取后有效图片路径
    valid_imgs(file_name, input_path, output_path)
