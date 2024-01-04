import os
import shutil
baseDir = os.path.normpath(r'D:\data\w_label(err')
objDir = os.path.normpath(r'D:\data\w_label_test')
folders=os.listdir(baseDir)
name=['Breast.nii.gz','P0.nii.gz','P1_reg.nii.gz','Tissues.nii.gz']
for folder in folders:
    files=os.listdir(baseDir+"\\"+folder)
    print(folder[-3:])
    print(files)
    for file in files:
        os.chdir(baseDir+"\\"+folder)
        if file==name[0]:
            shutil.copy(baseDir+"\\"+folder+"\\"+file,objDir+"\\"+"breast")
            os.chdir(objDir+"\\"+"breast")
            os.rename(file,"Breast_"+folder[-3:]+".nii.gz")
        elif file==name[1]:
            shutil.copy(baseDir+"\\"+folder+"\\"+file,objDir+"\\"+"raw")
            os.chdir(objDir+"\\"+"raw")
            os.rename(file,"Breast_"+folder[-3:]+"_0000.nii.gz")
        elif file==name[3]:
            shutil.copy(baseDir+"\\"+folder+"\\"+file,objDir+"\\"+"tissue")
            os.chdir(objDir+"\\"+"tissue")
            os.rename(file,"Breast_"+folder[-3:]+".nii.gz")

    