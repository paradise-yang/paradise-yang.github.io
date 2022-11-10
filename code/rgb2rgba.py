from PIL import Image
import os

path = "F:\data\yan-ji-ci\images/"# 原始路径
save_path = 'F:\data\yan-ji-ci\images-3c/'# 保存路径
all_images = os.listdir(path)

for image in all_images:
    image_path = os.path.join(path, image)
    img = Image.open(image_path)  # 打开图片
    print(img.format, img.size, img.mode, image_path)#打印出原图格式
    img = img.convert("RGB")  # 4通道转化为rgb三通道
    img.save(save_path + image)
