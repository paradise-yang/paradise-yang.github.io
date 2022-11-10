import imageio
import os

def create_gif(img_dir, image_list, gif_name, duration=0.05):
    frames = []
    for image_name in image_list:
        print("image_name={0} img_dir={1}".format(image_name, img_dir))
        frames.append(imageio.imread(img_dir + '/'+ image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return

def main():
    img_dir = 'F:\data\gyh/all'
    duration = 0.04 # 每秒20帧
    gif_name = img_dir+'.gif'
    image_list = os.listdir(img_dir + '/')
    create_gif(img_dir, image_list, gif_name, duration)

if __name__ == '__main__':
    main()