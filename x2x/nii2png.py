import os
import nibabel as nib
import imageio
import numpy as np
from tqdm import tqdm
 
def nii_to_image(filepath, imgfile):
    filenames = os.listdir(filepath)  # 读取nii文件夹
    with tqdm(total = len(filenames)) as pbar:
        for f in filenames:
            if f[-7:] != ".nii.gz":
                continue
            img_path = os.path.join(filepath, f)
            img = nib.load(img_path)  # 读取nii
            img_fdata = img.get_fdata(dtype=np.float32)  # 读取为float32
            fname = f.replace('.nii.gz', '')  # 去掉nii的后缀名
            img_f_path = os.path.join(imgfile, fname)
            # 创建nii对应的图像的文件夹
            if not os.path.exists(img_f_path):
                os.mkdir(img_f_path)  # 新建文件夹
 
            # 将归一化的浮点数数据转换为8位整数数据
            img_fdata = (img_fdata * 255).astype(np.uint8)
 
            # 开始转换为图像
            (x, y, z) = img.shape
            for i in range(z):  # z是图像的序列
                slice = img_fdata[:, :, i]  # 选择哪个方向的切片都可以
                # 保存图像，使用PNG格式
                imageio.imwrite(os.path.join(img_f_path, '{}.png'.format(i)), slice)
            pbar.update(1)
 
file_name = r"D:/data/TAO_MRI/T2/mask/seg_cut"
img_path = r"D:/data/TAO_MRI/T2/mask/seg_slice"
nii_to_image(file_name, img_path)