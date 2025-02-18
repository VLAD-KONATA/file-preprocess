import os
import nibabel as nib
import imageio
import numpy as np
from tqdm import tqdm

def normalize(slice):
    """Normalize the image slice to [0, 255]"""
    min_val = np.min(slice)
    max_val = np.max(slice)
    if max_val - min_val > 0:
        return ((slice - min_val) / (max_val - min_val) * 255).astype(np.uint8)
    else:
        return np.zeros_like(slice, dtype=np.uint8)

def nii_to_image(baseDir,objDir):
    files = os.listdir(baseDir)  # 读取nii文件夹
    with tqdm(total = len(files)) as pbar:
        for file in files:
            if  ".nii.gz" not in file:
                continue
            fname = file.replace('.nii.gz', '')  # 去掉nii的后缀名
            img_f_path = os.path.join(objDir, fname)
            # 创建nii对应的图像的文件夹
            if not os.path.exists(img_f_path):
                os.mkdir(img_f_path)  # 新建文件夹

            img_path = os.path.join(baseDir, file)
            img = nib.load(img_path)  # 读取nii
            img_fdata = img.get_fdata()
            img_fdata = np.rot90(img_fdata)

            
 
            # 开始转换为图像
            (x, y, z) = img.shape #img(240，150，50),img_fdata(150, 240, 50)
            for i in range(z):  # z是图像的序列
                slice = img_fdata[:,:, i]  # 选择哪个方向的切片都可以
                if x!=y:
                    # 计算需要填充的数量                    
                    target_z=256
                    pad_top = (target_z - y) // 2
                    pad_bottom = target_z - y - pad_top
                    pad_left=(target_z - x) // 2
                    pad_right=target_z-x-pad_left
                    #slice=np.rot90(slice)
                    # 使用零填充或复制边缘像素填充
                    padded_slice = np.pad(slice, ((pad_top, pad_bottom), (pad_left, pad_right)), mode='constant',constant_values = (-1000,-1000))
                    slice_normalized = normalize(padded_slice)
                else:
                    slice_normalized = normalize(slice)
                # 保存图像，使用PNG格式
               
                imageio.imwrite(os.path.join(img_f_path, '{}.png'.format(i)), slice_normalized)
            pbar.update(1)


#baseDir = r"/home/konata/Dataset/TED_MRI/T2/mask/origin/"
#objDir= r"/home/konata/Dataset/TED_MRI/T2/mask/origin_slice/TED_png"
#baseDir = r"/home/konata/Dataset/I3Net/CT/test"
baseDir = r"/home/konata/Dataset/TED_MRI/TOM500/val/image"
#objDir= r"/home/konata/Dataset/I3Net/slice_jpg/train"
#objDir= r"/home/konata/Dataset/I3Net/CT/test_slice"
objDir= r"/home/konata/Dataset/TED_MRI/TOM500/slice"
if not os.path.exists(objDir):
    os.mkdir(objDir)  # 新建文件夹
nii_to_image(baseDir,objDir)
