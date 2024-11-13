import SimpleITK as sitk
import os
import shutil

def crop_image(input_image, roi_start, roi_size):
    # 使用给定的ROI起始点和大小裁剪图像
    return sitk.RegionOfInterest(input_image, size=roi_size, index=roi_start)

def process_images(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".nii") or filename.endswith(".nii.gz"):  # 调整为你的图像格式
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            shape=[]
            # 设置ROI的起始点和大小（根据实际情况调整）
            # ROI的起始坐标 (x, y, z)
            roi_size = [300, 200, 70]  # ROI的大小 (x_size, y_size, z_size)
            print(f"Cropping {filename}")
            try:
                # 读取图像
                image = sitk.ReadImage(input_path)
                image_arr=sitk.GetArrayFromImage(image)
                shape=[image_arr.shape[2],image_arr.shape[1],image_arr.shape[0]]
                if 100<shape[2]<=110:
                    roi_start=[int(shape[0]/2-roi_size[0]/2),50,30]
                elif shape[2]<=100:
                    roi_start=[int(shape[0]/2-roi_size[0]/2),50,0]
                    roi_size[2]=int(shape[2])
                #elif shape[2] == 300:
                #   roi_start=[0,0,30]
                #   roi_size = [300, 200, 70]
                else:
                    roi_start=[int(shape[0]/2-roi_size[0]/2),50,30]

                # 裁剪图像
                cropped_image = crop_image(image, roi_start, roi_size)
                
                # 保存裁剪后的图像
                sitk.WriteImage(cropped_image, output_path)
            except:
                err_directory= "/home/konata/Dataset/TAO_CT/ERROR/"
                shutil.move(input_path,os.path.join(err_directory,filename))
            print(f"Cropped and saved {filename}")

if __name__ == "__main__":
    baseDir="/home/konata/Dataset/TAO_CT/TAO(复件)"
    z=set()
    folders=os.listdir(baseDir)
    for folder in folders:
        files=os.listdir(os.path.join(baseDir,folder))
        for file in files:
            image = sitk.ReadImage(os.path.join(baseDir,folder,file))
            image_arr=sitk.GetArrayFromImage(image)
            z.add(image_arr.shape[0])

    print(z)
    '''
    baseDir = "/home/konata/Dataset/TAO_CT/test/"  
    baseDir2 = "/home/konata/Dataset/TAO_CT/testcut/"  
    err_directory= "/home/konata/Dataset/TAO_CT/testERROR/"
    
    
    # 确保输出目录存在
    if not os.path.exists(baseDir2):
        os.makedirs(baseDir2)
    folders=os.listdir(baseDir2)
    if not os.path.exists(err_directory):
        os.makedirs(err_directory)
    '''
    for folder in folders:
        input_directory=os.path.join(baseDir,folder)    # 输入图像文件夹路径
        output_directory = os.path.join(baseDir,folder)  # 输出图像文件夹路径
    '''
        # 批量处理图像
        #process_images(input_directory, output_directory)
    process_images(baseDir, baseDir2)
    '''

