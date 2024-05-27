import SimpleITK as sitk
import os
import shutil


def get_error_folderslist():
    error_list = []
    folders = os.listdir(baseDir)
    for folder in folders:
        files = os.listdir(baseDir + "//" + folder)
        for file in files:
            img= sitk.ReadImage(baseDir+"//"+folder+"//"+file)
            #data_size = sitk.GetArrayFromImage(img).shape
            data_size = img.GetSize()
            if file=="Tissues.nii.gz":
                print(folder +"/"+file+ ":")
                print(data_size)
            '''if file == "Tissues.nii.gz":
                img = sitk.ReadImage(baseDir + "//" + folder + "//" + file)
                data_size = sitk.GetArrayFromImage(img).shape
                sizes = len(data_size)
                if sizes > 3:
                    error_list.append(folder)
                    print(folder + ":")
                    print(data_size)'''
    #return error_list


baseDir = os.path.normpath(
    r'/home/bo/PycharmProjects/iterative-cycle-consistent-semi-supervised-learning-for-fibroglandular-tissue-segmentation/data/w_label')
objDir = os.path.normpath(
    r'/home/bo/PycharmProjects/iterative-cycle-consistent-semi-supervised-learning-for-fibroglandular-tissue-segmentation/data/error')

get_error_folderslist()
'''error_list = get_error_folderslist()
for folder in error_list:
    source = (baseDir + "\\" + folder).replace("\\", "/")
    destination = (objDir + "\\" + folder).replace("\\", "/")
    # if os.path.exists(destination+"\\"+folder):
    # os.remove(destination+"\\"+folder)
    shutil.move(source, destination)'''
