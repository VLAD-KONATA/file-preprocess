import os
import numpy as np
from PIL import Image
import SimpleITK as sitk
from skimage import img_as_float  # 用于确保图像数据类型一致
from pathlib import Path

def png2nii(input,output,name):
    # 获取所有jpg文件列表
    image_files = sorted([os.path.join(input, f) for f in os.listdir(input) if f.endswith('.jpg')])

    # 初始化一个空的3D数组来存放所有的图像数据
    # 假设所有图片都是512x512大小
    image_shape =Image.open(image_files[0]) .size
    data_3d = np.zeros((len(image_files), image_shape[1],image_shape[0] ), dtype=np.float32)

    # 逐个读取JPG文件并填充到3D数组中
    for idx, image_file in enumerate(image_files):
        img = Image.open(image_file).convert('L')  # 转换为灰度图
        img_array = np.array(img)
        img_array=np.rot90(img_array)
        img_array=np.rot90(img_array)
        # 确保所有图像数据具有相同的数据类型和范围
        img_array = img_as_float(img_array)
        
        data_3d[idx, :,: ] = img_array

    # 创建NIfTI图像对象
\
    #spacing=(0.9375,0.9375,0.6)
    #samp=sitk.ReadImage(os.path.join('/home/konata/Dataset/I3Net/imagesTs/IXI013-HH-1212-T2.nii.gz'))
    spacing=(0.3125,0.3125,3.85/2)
    #origin spacing(0.3125,0.3125,3.85)-TEDMRI-T2(512,512,20)
    #samp=sitk.ReadImage(os.path.join('/home/konata/Dataset/TED_MRI/T2/mask/origin',name))
    
    # spacing=(0.5566,0.5566,1/4)
    #origin spacing(0.5566,0.5566,1)-TAOCT(240,150,50)
    #samp=sitk.ReadImage(os.path.join('/home/konata/Dataset/I3Net/CT/test/',name))
    
    samp=sitk.ReadImage(os.path.join('/home/konata/Dataset/TED_MRI/TOM500/all_image',name))
    samp=sitk.Image(samp)
    outs = sitk.GetImageFromArray(data_3d)
    outs.SetDirection(samp.GetDirection())
    outs.SetOrigin(samp.GetOrigin())
    outs.SetSpacing(spacing)
    sitk.WriteImage(outs,output) #输出图像


    print(f"Saved NIfTI file to {output}")

if __name__=='__main__':
    # 定义输入和输出路径
    #input_dir = '/home/konata/Dataset/I3Net/RIFE_test/IXI012-HH-1211-T2_fpsx2'  # 替换为你的jpg文件所在目录
    #output_file = '/home/konata/Dataset/I3Net/RIFE_test/test.nii.gz'  # 输出的nii.gz文件名
    #input_dir = '/home/konata/Dataset/TED_MRI/T2/mask/origin_slice/RIFE_test_fpsx4'  # 替换为你的jpg文件所在目录
    #output_dir = '/home/konata/Dataset/TED_MRI/T2/mask/origin_slice/RIFE_test_nii_fpsx4/'  # 输出的nii.gz文件名
    #input_dir = '/home/konata/Dataset/I3Net/CT/test_fpsx4/RIFE_test_fpsx4'  # 替换为你的jpg文件所在目录
    #output_dir = '/home/konata/Dataset/I3Net/CT/test_fpsx4/RIFE_test_nii_fpsx4/'  # 输出的nii.gz文件名
    #input_dir = '/home/konata/Dataset/TED_MRI/TOM500/test_fpsx4_2025_01_16_16_58_21/RIFE_test_fpsx4'  # 替换为你的jpg文件所在目录
    #output_dir = '/home/konata/Dataset/TED_MRI/TOM500/test_fpsx4_2025_01_16_16_58_21/RIFE_test_nii_fpsx4/'  # 输出的nii.gz文件名
    input_dir = '/home/konata/Dataset/TED_MRI/TOM500/test_fpsx2_2025_01_06_23_26_55/RIFE_test_fpsx2'  # 替换为你的jpg文件所在目录
    output_dir = '/home/konata/Dataset/TED_MRI/TOM500/test_fpsx2_2025_01_06_23_26_55/RIFE_test_nii_fpsx2/'  # 输出的nii.gz文件名
    Path(output_dir).mkdir(exist_ok=True, parents=True)
    folders=os.listdir(input_dir)
    for folder in folders:
        name=folder.split('_fps')[0]+'.nii.gz'
        png2nii(os.path.join(input_dir,folder),os.path.join(output_dir,name),name)
