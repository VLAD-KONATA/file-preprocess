import os
import shutil

baseDir1 = os.path.normpath(
    r'/home/bo/PycharmProjects/iterative-cycle-consistent-semi-supervised-learning-for-fibroglandular-tissue-segmentation/data/label/breast')
baseDir2 = os.path.normpath(
    r'/home/bo/PycharmProjects/iterative-cycle-consistent-semi-supervised-learning-for-fibroglandular-tissue-segmentation/data/label/DandV')
objDir = os.path.normpath(
    r'/home/bo/PycharmProjects/iterative-cycle-consistent-semi-supervised-learning-for-fibroglandular-tissue-segmentation/data/w_label')
if not os.path.exists(objDir):
    os.makedirs(objDir)

fileslist = os.listdir(baseDir1)

for file in fileslist:
    source = (baseDir1 + "\\" + file).replace("\\", "/")
    destination = (objDir + "\\" + file[:-14] + "\\").replace("\\", "/")

    # if os.path.exists(destination+"\\"+file):
    #    os.remove(destination+"\\"+file)
    shutil.move(source, destination)
