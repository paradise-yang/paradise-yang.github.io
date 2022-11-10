import cv2

def Video_fetching(input_path, save_path, frame_interval):
    cap = cv2.VideoCapture()                                   # 初始化一个VideoCapture对象
    filename = input_path.split("/")[-1][:-4]
    if input_path.endswith('.MP4'):
        cap.open(input_path)                                   # VideoCapture::open函数可以从文件获取视频
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))      # 获取视频帧数
        for i in range(20):
            cap.read()
        k = 0
        for i in range(n_frames-20):                           # 为了避免视频头几帧质量低下，黑屏或者无关等
            ret, frame = cap.read()
            if i % frame_interval == 0:                        # 每隔frame_interval帧进行一次截屏操作
                imagepath = save_path + str("%05d" % k) +".png"
                print('exported {}!'.format(imagepath))
                k = k + 1
                try:
                    frame_n = cv2.resize(frame, (1920, 1080))  # 所需图片分辨率
                    cv2.imwrite(imagepath, frame_n)
                except Exception as e:
                    print(e)
    else:
        print('This file is not video')
    cap.release()

if __name__ == "__main__":
    input_path = "F:\data\xue/temp.MP4"     # 视频输入路径
    save_path = "F:\data\xue\img/"                 # 提取图片输出路径
    frame_interval = 10                                         # 提取帧的间隔数
    Video_fetching(input_path, save_path, frame_interval)
