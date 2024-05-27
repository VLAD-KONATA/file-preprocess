import os

baseDir = os.path.normpath(r'/home/bo/PycharmProjects/iterative-cycle-consistent-semi-supervised-learning-for-fibroglandular-tissue-segmentation/data/w_label/')
folders=os.listdir(baseDir)
name=['Breast.nii.gz', 'P0.nii.gz', 'P1_reg.nii.gz', 'Tissues.nii.gz']

for folder in folders:
    files = os.listdir(baseDir + "/" + folder)
    for file in files:
        os.chdir(baseDir + "/" + folder)
        if file == folder + "_Breast.nii.gz":
            os.rename(file, name[0])
        elif file == folder + "_Dense_and_Vessels.nii.gz":
            os.rename(file, name[3])
        '''if file == folder + "_1st.nii.gz":
            os.rename(file, name[2])
        elif file == folder + "_pre.nii.gz":
            os.rename(file, name[1])
        #elif file == folder + ".nii.gz":
        #    os.rename(file, name[0])
        elif file == "Segmentation_" + folder + "_Breast.seg.nii.gz":
            os.rename(file, name[0])
        elif file == "Tissue.nii.gz":
            os.rename(file, name[3])
        #elif file == "Segmentation_" + folder + "_Dense_and_Vessels.seg.nii.gz":
        #    os.rename(file, name[3])
        '''
