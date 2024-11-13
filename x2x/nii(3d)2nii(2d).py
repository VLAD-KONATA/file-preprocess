import os
import SimpleITK as sitk
import numpy
import json
import tqdm

baseDir = r"/home/konata/Dataset/TED_MRI/T2/mask/seg_cut/"
baseDir2 = r"/home/konata/Dataset/TED_MRI/T2/mask/origin_cut/"
objDir=r"/home/konata/Dataset/TED_MRI/T2/mask/seg_slice/"
objDir2=r"/home/konata/Dataset/TED_MRI/T2/mask/origin_slice/"
if not os.path.exists(objDir):
    os.mkdir(objDir)
if not os.path.exists(objDir2):
    os.mkdir(objDir2)

with open('/home/konata/Dataset/TED_MRI/T2/mask/seg_unique.json', 'r') as file:
    unique=json.load(file)
print(unique)

list8=[]
for i in unique.items():
    if i[1][0]!=9:
          list8.append(i[0])
for i in list8:
    unique.pop(i)



tbar=tqdm.tqdm(unique.items())
for item in tbar:
    file=item[0]
    slice=item[1][1]
    if len(slice)>1 and len(slice)%2==1:
        i=slice[int(len(slice)/2)]
    elif len(slice)>1 and len(slice)%2==0:
        i=slice[int(len(slice)/2)-1]
    else:
        i=slice[0]
    seg=sitk.ReadImage(os.path.join(baseDir,file))
    seg=sitk.GetArrayFromImage(seg)
    outs = sitk.GetImageFromArray(seg[i,:,:])
    sitk.WriteImage(outs,os.path.join(objDir,file))

    origin=sitk.ReadImage(os.path.join(baseDir2,file))
    origin=sitk.GetArrayFromImage(origin)
    outo = sitk.GetImageFromArray(origin[i,:,:])
    sitk.WriteImage(outo,os.path.join(objDir2,file))
