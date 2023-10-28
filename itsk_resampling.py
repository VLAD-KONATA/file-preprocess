import os
import SimpleITK as sitk
 
def resampleVolume(outspacing, vol):
    """
    将体数据重采样的指定的spacing大小\n
    paras：
    outpacing：指定的spacing，例如[1,1,1]
    vol：sitk读取的image信息，这里是体数据\n
    return：重采样后的数据
    """
    outsize = [0, 0, 0]
    # 读取文件的size和spacing信息
    inputsize = vol.GetSize()
    inputspacing = vol.GetSpacing()
 
    transform = sitk.Transform()
    transform.SetIdentity()
    # 计算改变spacing后的size，用物理尺寸/体素的大小
    outsize[0] = round(inputsize[0] * inputspacing[0] / outspacing[0])
    outsize[1] = round(inputsize[1] * inputspacing[1] / outspacing[1])
    outsize[2] = round(inputsize[2] * inputspacing[2] / outspacing[2])
 
    # 设定重采样的一些参数
    resampler = sitk.ResampleImageFilter()
    resampler.SetTransform(transform)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetOutputOrigin(vol.GetOrigin())
    resampler.SetOutputSpacing(outspacing)
    resampler.SetOutputDirection(vol.GetDirection())
    resampler.SetSize(outsize)
    newvol = resampler.Execute(vol)
    return newvol
 
 

if __name__ == '__main__':
    baseDir = r'E:\breastxxx\Duke-Breast-Cancer-MRI-Supplement-v3\Segmentation_Masks_NIFTI'
    objDir = 'E:\\breastxxx\\Duke-Breast-Cancer-MRI-Supplement-v3\\resample_Segmentation_Masks_NIFTI'
    outspacing_0 = 1 
    outspacing_1 = 1
    outspacing_2 = 1
    
    #I_vol_list = ['reg_ADC.nii.gz', 'reg_DWI_0.nii.gz', 'reg_DWI_800.nii.gz', 'reg_T1C.nii.gz', 'T2.nii.gz']
 
    if os.path.exists(baseDir):
        folders = os.listdir(baseDir)
        for folder in folders:
            folder_dir = baseDir +"\\"+ folder
            imgs_list = os.listdir(folder_dir)
 
            for img in imgs_list:
                #if img in I_vol_list:
                img_dir = baseDir +"\\"+ folder + '\\' + img
                if not os.path.exists(objDir+"\\"+folder):
                    os.makedirs(objDir+"\\"+folder)
                resampled_img_dir = objDir +"\\"+ folder +"\\"+ img
 
                img_ori = sitk.Image(sitk.ReadImage(img_dir))
                img_ori_spacing = img_ori.GetSpacing()
                #outspacing_2 = img_ori_spacing[2]
                outspacing = [outspacing_0, outspacing_1, outspacing_2]
 
                img_resampled = resampleVolume(outspacing, img_ori)
                sitk.WriteImage(img_resampled, resampled_img_dir)
                print('pid_', folder, ' ', img, ' transformed!')             