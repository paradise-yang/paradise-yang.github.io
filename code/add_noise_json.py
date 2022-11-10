from email.contentmanager import raw_data_manager
import os
import json
import copy
import random
import trimesh
import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.linalg import *

def nerf_matrix_to_ngp(pose, scale=0.33):
    # for the fox dataset, 0.33 scales camera radius to ~ 2
    new_pose = np.array([
        [pose[1, 0], -pose[1, 1], -pose[1, 2], pose[1, 3] * scale],
        [pose[2, 0], -pose[2, 1], -pose[2, 2], pose[2, 3] * scale],
        [pose[0, 0], -pose[0, 1], -pose[0, 2], pose[0, 3] * scale],
        [0, 0, 0, 1],
    ], dtype=np.float32)
    return new_pose

def visualize_poses(poses, size=0.2):
    # poses: [B, 4, 4]
    axes = trimesh.creation.axis(axis_length=10)
    objects = [axes]

    for pose in poses:
        # a camera is visualized with 8 line segments.
        pos = pose[:3, 3]
        a = pos + size * pose[:3, 0] + size * pose[:3, 1] + size * pose[:3, 2]
        b = pos - size * pose[:3, 0] + size * pose[:3, 1] + size * pose[:3, 2]
        c = pos - size * pose[:3, 0] - size * pose[:3, 1] + size * pose[:3, 2]
        d = pos + size * pose[:3, 0] - size * pose[:3, 1] + size * pose[:3, 2]

        segs = np.array([[pos, a], [pos, b], [pos, c], [pos, d], [a, b], [b, c], [c, d], [d, a]])
        segs = trimesh.load_path(segs)
        objects.append(segs)

    trimesh.Scene(objects).show()

def add_noise_json(file_name, output_name):
    sigma_r = 5.0 # 旋转矩阵的噪声方差
    sigma_t = 0.1

    # 读取原位姿
    with open(file_name, 'r') as f:
        transform = json.load(f)
    frames = transform["frames"]
    frames = sorted(frames, key=lambda d: d['file_path'])
    
    transform["frames"] = []
    poses_ori = []
    poses_noise = []
    dict = copy.deepcopy(transform)
    num = 0
    scale = 0.33
    for frame in frames:
        pose_transform_matrix = np.array(frame['transform_matrix'], dtype=np.float32)
        poses_ori.append(
            nerf_matrix_to_ngp(
                np.array(frame['transform_matrix'], dtype=np.float32), scale=scale))
        # 旋转矩阵添加噪声
        pose_matrix = R.from_matrix([
            [pose_transform_matrix[0, 0], pose_transform_matrix[0, 1], pose_transform_matrix[0, 2]],
            [pose_transform_matrix[1, 0], pose_transform_matrix[1, 1], pose_transform_matrix[1, 2]],
            [pose_transform_matrix[2, 0], pose_transform_matrix[2, 1], pose_transform_matrix[2, 2]]
            ])
        pose_euler = pose_matrix.as_euler('zyx', degrees=True)
        noise = np.random.normal(loc=0.0, scale=sigma_r, size=3)
        pose_euler_noise = pose_euler + noise
        pose_euler = R.from_euler('zyx', pose_euler_noise, degrees=True)
        pose_matrix = pose_euler.as_matrix()
        # 平移向量添加噪声
        trans_vec = np.array(
            [pose_transform_matrix[0, 3], pose_transform_matrix[1, 3], pose_transform_matrix[2, 3]], 
            dtype=np.float32)
        noise = np.random.normal(loc=0.0, scale=sigma_t, size=3)
        trans_vec = trans_vec + noise
        for i in [0, 1, 2]:
            pose_transform_matrix[i, 0] = pose_matrix[i, 0]
            pose_transform_matrix[i, 1] = pose_matrix[i, 1]
            pose_transform_matrix[i, 2] = pose_matrix[i, 2]
            pose_transform_matrix[i, 3] = trans_vec[i]
        print(pose_transform_matrix)
        frame['transform_matrix'] =  pose_transform_matrix.tolist()
        poses_noise.append(
            nerf_matrix_to_ngp(
                np.array(pose_transform_matrix, dtype=np.float32), scale=scale))
        dict['frames'].append(frame)
        num = num + 1
    visualize_poses(poses_ori)
    visualize_poses(poses_noise)
    with open(output_name, "w") as outfile:
        json.dump(dict, outfile, indent=2)
    return num
 
 
if __name__=="__main__":
    file_name = "/data/paradise/code/neddf/data/nerf_synthetic/lego_noise/transforms_train.json"
    output_name = "/data/paradise/code/neddf/data/nerf_synthetic/lego_noise/transforms_train_noise.json"
    data = add_noise_json(file_name, output_name)
