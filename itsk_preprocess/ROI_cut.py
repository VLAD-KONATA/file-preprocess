import SimpleITK as sitk
import os
import shutil

def crop_image(input_image, roi_start, roi_size):
    # 使用给定的ROI起始点和大小裁剪图像
    return sitk.RegionOfInterest(input_image, size=roi_size, index=roi_start)

def process_images(input_dir, output_dir,filename):
    if filename.endswith(".nii") or filename.endswith(".nii.gz"):  # 调整为你的图像格式
        shape=[]
        # 设置ROI的起始点和大小（根据实际情况调整）
        # ROI的起始坐标 (x, y, z)
        print(f"Cropping {filename}")
        try:
            # 读取图像
            image = sitk.ReadImage(input_dir)
            image_arr=sitk.GetArrayFromImage(image)
            shape=[image_arr.shape[2],image_arr.shape[1],image_arr.shape[0]]
            roi_size = [shape[0],128,shape[2]]  # ROI的大小 (x_size, y_size, z_size)
            if shape[1]==256:
                roi_start=[0,int(shape[1])-int(roi_size[1])-1,0]
            elif shape[1]==255:
                roi_start=[0,int(shape[1])-int(roi_size[1]),0]

            # 裁剪图像
            cropped_image = crop_image(image, roi_start, roi_size)
            
            # 保存裁剪后的图像
            sitk.WriteImage(cropped_image, output_dir)
        except:
            pass
            #err_directory= "/home/konata/Dataset/TAO_CT/ERROR/"
            #shutil.move(input_dir,os.path.join(err_directory,filename))
        print(f"Cropped and saved {filename}")

if __name__ == "__main__":
    baseDir="/home/konata/Dataset/I3Net/imagesTs/"
    objDir="/home/konata/Dataset/I3Net/imagesTs_cut/"
    baseDir2="/home/konata/Dataset/I3Net/d2_slicex2_2025_03_02_21_30_09/esrgan_nii/"
    objDir2="/home/konata/Dataset/I3Net/d2_slicex2_2025_03_02_21_30_09/esrgan_nii_cut/"

    files=os.listdir(baseDir2)

    # 确保输出目录存在
    if not os.path.exists(objDir):
        os.makedirs(objDir)
    if not os.path.exists(objDir2):
        os.makedirs(objDir2)
    
    for file in files:
        input_directory=os.path.join(baseDir,file)    # 输入图像文件夹路径
        output_directory = os.path.join(objDir,file)  # 输出图像文件夹路径        
        input_directory2=os.path.join(baseDir2,file)    # 输入图像文件夹路径
        output_directory2 = os.path.join(objDir2,file)  # 输出图像文件夹路径
        # 批量处理图像
        process_images(input_directory, output_directory,file)
        process_images(input_directory2, output_directory2,file)

