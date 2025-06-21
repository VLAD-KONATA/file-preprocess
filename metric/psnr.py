import SimpleITK as sitk
import cv2
from skimage.metrics import peak_signal_noise_ratio as psnr
import numpy as np
import os
import lpips
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import torch
def compute_psnr(file,nii_path_1, nii_path_2):
    """
    计算两个NIfTI图像之间的PSNR。
    
    参数:
        nii_path_1: 第一个NIfTI图像的路径。
        nii_path_2: 第二个NIfTI图像的路径。
        
    返回:
        PSNR值。
    """
    # 读取NIfTI图像
    img1 = sitk.ReadImage(nii_path_1)
    img2 = sitk.ReadImage(nii_path_2)
    
    # 将SimpleITK图像转换为numpy数组
    img1_array = sitk.GetArrayFromImage(img1).astype(np.float32)
    img2_array = sitk.GetArrayFromImage(img2).astype(np.float32)
    '''
    img1_array=img1_array[1:126]
    print(img1_array.shape)
    # 确保两个图像具有相同的形状
    if img1_array.shape != img2_array.shape:
        raise ValueError("The shape of the two images does not match.")
    '''
    for i in range(img2_array.shape[0]):
        
        # 计算数据范围
        data_range = np.max(img1_array) - np.min(img1_array)
        
        # 如果数据范围为0（即所有像素值相同），则直接返回PSNR为无穷大
        if data_range == 0:
            return float('inf')
        # 计算PSNR
        try:
            psnr_value = psnr(img1_array[i+2], img2_array[i], data_range=data_range)
            print(f"The PSNR between the two images {file} [{i}]is: {psnr_value:.2f} dB")
            
            #print(psnr_value)
        except Exception as e:
            print(f"Error during PSNR calculation: {e}")
            return None
    return psnr_value

def compute_psnr2d(folder,file,path_1, path_2,txtpath):
    # 读取NIfTI图像
    img1 = cv2.imread(path_1)
    img2 = cv2.imread(path_2)
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')  # 没有差异时PSNR为无穷大
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    print(f"{folder}-{file} PSNR value is {psnr} dB")
    with open(txtpath,'a+') as txt:
            txt.writelines(f"{folder}-{file} PSNR value is {psnr} dB\n")
    return psnr

    # 将SimpleITK图像转换为numpy数组

def compute_lpips(folder,file,path_1, path_2,txtpath):
    # 加载预训练的LPIPS模型


    # 初始化 LPIPS 模型（例如，使用 vgg 预训练模型）
    lpips_model = lpips.LPIPS(net='vgg')  # 也可以选择 'alex' 或 'squeeze'

    # 如果有 GPU，将模型移到 GPU 上
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    lpips_model.to(device)

    # 加载两幅图像
    image1 = Image.open(path_1).convert('RGB')
    image2 = Image.open(path_2).convert('RGB')

    # 对图像进行预处理
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    image1 = preprocess(image1).unsqueeze(0).to(device)
    image2 = preprocess(image2).unsqueeze(0).to(device)
    with torch.no_grad():
        # 使用LPIPS模型计算相似性
        similarity_score = lpips_model(image1, image2)

    print(f"{folder}-{file} LPIPS Similarity is {similarity_score.item()}")

# 使用示例
#nii_file_1 = r'/home/konata/Dataset/I3Net/imagesTs/'  # 替换为你的第一个NIfTI文件路径
#nii_file_1 = '/home/konata/Dataset/IXI-T2/origin_test_slice'  # 替换为你的第二个NIfTI文件路径
nii_file_1 = '/home/konata/Dataset/IXI-T2/origin_ct_slice'  # 替换为你的第二个NIfTI文件路径
#nii_file_2='/home/konata/Dataset/IXI-T2/mnet/IXI_test_slice'
#nii_file_2='/home/konata/Dataset/IXI-T2/I3Net/test_slice'
#nii_file_2='/home/konata/Dataset/IXI-T2/mnet/TAOCT_test_slice'
nii_file_2='/home/konata/Dataset/IXI-T2/I3Net/test_ct_slice'

txtpath ='/home/konata/Dataset/IXI-T2/test_psnr_ct_I3Net.txt'
#txtpath ='/home/konata/Dataset/IXI-T2/test_psnr_ct_mnet.txt'
#txtpath ='/home/konata/Dataset/IXI-T2/test_psnr_ixi_I3Net.txt'
#txtpath ='/home/konata/Dataset/IXI-T2/test_psnr_ixi_mnet.txt'
nii=False
mode='psnr'

if nii:
    files=os.listdir(nii_file_2)
    for file in files:
        origin=os.path.join(nii_file_1,file)
        a=os.path.join(nii_file_2,file)
        psnr_result = compute_psnr(file,origin, a)

    '''
        if psnr_result is not None:
            print(f"The PSNR between the two images {file} is: {psnr_result:.2f} dB")
        else:
            print("Failed to calculate PSNR.")
    '''
else:
    folders=os.listdir(nii_file_2)
    folders.sort(key=lambda x:int(x.split('IXI')[-1].split('-')[0]))
    avg_psnr_all=0

    for folder in folders:
        psnr_all=0
        num=0
        files= os.listdir(os.path.join(nii_file_2,folder))
        #files.sort(key=lambda x:int(x.split('_out.png')[0]))    #I3Net+esrgan
        #files.sort(key=lambda x:int(x.split('.jpg')[0]))    #RIFE
        #files.sort(key=lambda x:int(x.split('_out.jpg')[0]))    #RIFE+esrgan
        files.sort(key=lambda x:int(x.split('.png')[0].split('/')[-1])) #I3Net

        for file in files:
            #if int(file.split('.png')[0])%2==0:
                #continue
            #origin=os.path.join(nii_file_1,folder,file.split('_out.png')[0]+'.png') #I3Net+esrgan
            #origin=os.path.join(nii_file_1,folder.split('_fpsx2')[0],str(int(file.split('.jpg')[0]))+'.png') #origin-RIFE
            #origin=os.path.join(nii_file_1,folder,str(int(file.split('_out.jpg')[0]))+'.png') #origin-RIFE-esrgan
            origin=os.path.join(nii_file_1,folder,file.split('.png')[0]+'.png') #   I3Net
            a=os.path.join(nii_file_2,folder,file)
            if mode =='lpips':
                compute_lpips(folder,file,origin,a,txtpath)
            elif mode=='psnr':
                psnr_result = compute_psnr2d(folder,file,origin, a,txtpath)
                #if psnr_result==float('inf'):
                if psnr_result>45:
                    continue
                psnr_all+=psnr_result
                num+=1
        psnr_avg=psnr_all/num
        print(f"{folder} avg PSNR value is {psnr_avg} dB")
        with open(txtpath,'a+') as txt:
            txt.writelines(f"{folder} avg PSNR value is {psnr_avg} dB\n")
        avg_psnr_all+=psnr_avg

    all_avg=avg_psnr_all/len(folders)
    print(f"all avg PSNR value is {all_avg} dB")
    with open(txtpath,'a+') as txt:
        txt.writelines(f"all avg PSNR value is {all_avg} dB\n")