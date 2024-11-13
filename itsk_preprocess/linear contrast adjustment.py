import SimpleITK as sitk
import os
import shutil

def adjust_contrast(input_image, minimum, maximum, level, window):
    # Convert level and window to upper and lower bounds
    lower_bound = level - window / 2.0
    upper_bound = level + window / 2.0
    
    # Clip image values to [minimum, maximum]
    clipped_image = sitk.Threshold(input_image, lower=minimum, upper=maximum, outsideValue=minimum)
    
    # Rescale the intensity of the image to the desired range [lower_bound, upper_bound]
    rescaled_image = sitk.RescaleIntensity(clipped_image, outputMinimum=lower_bound, outputMaximum=upper_bound)
    
    return rescaled_image

def process_images(input_dir, output_dir, minimum, maximum, level, window):
    for filename in os.listdir(input_dir):
        if filename.endswith(".nii") or filename.endswith(".nii.gz"):  # Adjust to your image format
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            # Read the image
            image = sitk.ReadImage(input_path)
            print(f"Processing {filename}")
            # Adjust contrast
            try:
                adjusted_image = adjust_contrast(image, minimum, maximum, level, window)
            except:
                shutil.move(input_path,'/home/konata/Dataset/TAO_CT/ERROR/'+filename)
            # Save the adjusted image
            sitk.WriteImage(adjusted_image, output_path)
            print(f"Processed {filename}")

if __name__ == "__main__":
    base_directory = "/home/konata/Dataset/TAO_CT/test"  
    folders=os.listdir(base_directory)
    
    # 设置对比度调整参数
    minimum_value = -1024
    maximum_value = 1631
    level_value = 303.5
    window_value = 2655
    '''
    for folder in folders:
        input_directory  = os.path.join(base_directory,folder)    # 输入图像文件夹路径
        output_directory = os.path.join(base_directory,folder)  # 输出图像文件夹路径
        # 确保输出目录存在
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
    '''
    input_directory=base_directory
    output_directory=base_directory

    # 批量处理图像
    process_images(input_directory, output_directory, minimum_value, maximum_value, level_value, window_value)
