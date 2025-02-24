import os
import numpy as np
from PIL import Image
import SimpleITK as sitk
from skimage import img_as_float  # 用于确保图像数据类型一致
from pathlib import Path

def niid2(inpath,outpath,name):
    img=sitk.ReadImage(os.path.join(inpath,name))
    img=sitk.Image(img)
    array=sitk.GetArrayFromImage(img)
    shape=array.shape
    zero=array[::2]
    '''
    zero=np.zeros(((shape[0]+1)/2,shape[1],shape[2]),dtype=np.float32)
    for i in range(shape[0]):
        zero[i,:,:]=array[i*2,:,:]
    '''
    spacing=(0.3125,0.3125,3.85)
    outs=sitk.GetImageFromArray(zero)
    outs.SetDirection(img.GetDirection())
    outs.SetOrigin(img.GetOrigin())
    outs.SetSpacing(spacing)
    sitk.WriteImage(outs,os.path.join(outpath,name))
    print(f"Saved NifTI file to {os.path.join(outpath,name)}")


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
    input_dir = 'C:/Users/VLADKONATA/Desktop/receive/seg'  # 替换为你的jpg文件所在目录
    output_dir = 'C:/Users/VLADKONATA/Desktop/receive/segd2'  # 输出的nii.gz文件名
    Path(output_dir).mkdir(exist_ok=True, parents=True)
    files=os.listdir(input_dir)
    for name in files:
        niid2(input_dir,output_dir,name)
