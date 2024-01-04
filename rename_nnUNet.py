import os
import shutil
baseDir = os.path.normpath(r'/home/bo/Gao_win/nnUNet/DATASET/nnUNet_raw/Dataset012_Breast/rawdata')
objDir = os.path.normpath(r'/home/bo/Gao_win/nnUNet/DATASET/nnUNet_raw/Dataset012_Breast')
folders=os.listdir(baseDir)
name=['Breast.nii.gz','P0.nii.gz','P1_reg.nii.gz','Tissues.nii.gz']
for folder in folders:
    files=os.listdir(baseDir+"/"+folder)
    print(folder[-3:])
    print(files)
    for file in files:
        os.chdir(baseDir+"/"+folder)
        if file==name[0]:
            shutil.copy(baseDir+"/"+folder+"/"+file,objDir+"/"+"imagesTr(b")
            os.chdir(objDir+"/"+"imagesTr(b")
            os.rename(file,"Breast_"+folder[-3:]+".nii.gz")
        elif file==name[1]:
            shutil.copy(baseDir+"/"+folder+"/"+file,objDir+"/"+"imagesTr")
            os.chdir(objDir+"/"+"imagesTr")
            os.rename(file,"Breast_"+folder[-3:]+"_0000.nii.gz")
        elif file==name[3]:
            shutil.copy(baseDir+"/"+folder+"/"+file,objDir+"/"+"labelsTr")
            os.chdir(objDir+"/"+"labelsTr")
            os.rename(file,"Breast_"+folder[-3:]+".nii.gz")

    
