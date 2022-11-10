import cv2
import os
from cv2 import imshow, bitwise_not

def add_mask2image_binary(original_path, ori_mask_path, images_path, masks_path):
    for ori_item in os.listdir(original_path):
        print(ori_item)                                               # 输出正在处理的图片
        ori_path = os.path.join(original_path, ori_item)              # 原始图片路径
        ori = cv2.imread(ori_path)                                    # 读取原始图片

        mask_path = os.path.join(ori_mask_path, ori_item)             
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)            # 将彩色mask以二值图像形式读取
        _,new_mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)   # 根据所需填充颜色，这里是填充白色，只要不是黑色(0)就填充白色(255)
        new_mask = cv2.cvtColor(new_mask, cv2.COLOR_GRAY2RGB)
        cv2.imwrite(os.path.join(masks_path, ori_item),new_mask)
        temp = cv2.bitwise_not(new_mask)                              # 反转黑白用于提取

        image = cv2.bitwise_or(ori, temp)
        cv2.imwrite(os.path.join(images_path, ori_item), image)

original_path = 'F:\data/yzn/small/' # 原始图片路径
ori_mask_path = 'F:\data/yzn/old/' # 原始红色mask路径
images_path = 'F:\data/yzn/up/' # 分割后图片路径
masks_path = 'F:\data/yzn/new/' # 修改颜色后mask路径
add_mask2image_binary(original_path, ori_mask_path, images_path, masks_path)
