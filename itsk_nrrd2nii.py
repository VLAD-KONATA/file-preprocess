import SimpleITK as sitk
from glob import glob
import os

baseDir = os.path.normpath(r'E:/breastxxx/Duke-Breast-Cancer-MRI-Supplement-v3/Segmentation_Masks_NRRD/')
objDir=baseDir[:-23]+"Segmentation_Masks_NIFTI"
if not os.path.exists(objDir):
    os.makedirs(objDir)
folders=os.listdir(baseDir)
for folder in folders:
    if not os.path.exists(objDir+"\\"+folder):
        os.makedirs(objDir+"\\"+folder)
    files=glob(baseDir+"\\"+folder+'/*seg.nrrd')
    for file in files:
        img = sitk.ReadImage(file)
        sitk.WriteImage(img, objDir+"\\"+file[74:-4]+"nii.gz")