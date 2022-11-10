import os
from unicodedata import name

path = 'F:\data\yzn/new/'      # 文件夹路径
out_path = 'F:\data\yzn\masks/'
start = 0                # 重命名后第一个图片序号

for img in os.listdir(path):
    name = "%05d" % start #5位数 不足前面补零
    print(name)
    os.rename(path + img, out_path + name + ".png")
    start = start + 1
