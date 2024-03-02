import SimpleITK as sitk
import numpy
import os
baseDir=r'C:/Users/VLADKONATA/Desktop/quality test/gd/'
objDir=r'C:/Users/VLADKONATA/Desktop/quality test/gd(process)/'
if not os.path.exists(objDir):
    os.makedirs(objDir)
masklist=os.listdir(baseDir)
for maskname in masklist:
    mask= sitk.Image(sitk.ReadImage(baseDir+maskname))
    mask_arr=sitk.GetArrayFromImage(mask)
    mask_arr[mask_arr == 1] = 0
    mask_arr[mask_arr == 2] = 1
    img_itk = sitk.GetImageFromArray(mask_arr)
    sitk.WriteImage(img_itk, objDir+maskname)
    print(maskname+" process complete")