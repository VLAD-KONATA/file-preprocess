import os
flag=0

if flag==True:
    baseDir = os.path.normpath(
        r'/home/bo/PycharmProjects/iterative-cycle-consistent-semi-supervised-learning-for-fibroglandular-tissue-segmentation/data/w_label')

    dirs = os.listdir(baseDir)

    f = open('../data/train.txt', 'w+')
    for dir in dirs:
        f.writelines("w-" + dir + "\n")
    baseDir = os.path.normpath(
        r'/home/bo/PycharmProjects/iterative-cycle-consistent-semi-supervised-learning-for-fibroglandular-tissue-segmentation/data/wo_label')
    dirs = os.listdir(baseDir)
    for dir in dirs:
        f.writelines("wo-" + dir + "\n")
    f.close()
else:
    baseDir = os.path.normpath(
        r'/home/bo/PycharmProjects/iterative-cycle-consistent-semi-supervised-learning-for-fibroglandular-tissue-segmentation/data/w_label')

    dirs = os.listdir(baseDir)

    f = open('../data/test.txt', 'w+')
    for dir in dirs:
        f.writelines(dir + "\n")
    f.close()

