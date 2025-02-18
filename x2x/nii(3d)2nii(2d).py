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

print(len(unique))
unique = dict(sorted(unique.items(), key=lambda item: int(item[0].split('_')[0])))

#SLICE(NO L/R)
'''
tbar=tqdm.tqdm(unique.items())
a=1
for item in tbar:
    file=item[0]
    slice=item[1][1]
    
    seg=sitk.ReadImage(os.path.join(baseDir,file))
    origin=sitk.ReadImage(os.path.join(baseDir2,file))
    spacing=seg.GetSpacing()
    origin=seg.GetOrigin()
    direction=seg.GetDirection()
    size=seg.GetSize()
    
    for i in slice:
        seg=sitk.ReadImage(os.path.join(baseDir,file))
        seg=sitk.GetArrayFromImage(seg)
        outs = sitk.GetImageFromArray(seg[i-1,:,:])
        sitk.WriteImage(outs,os.path.join(objDir,str(a)+'.nii.gz'))

        origin=sitk.ReadImage(os.path.join(baseDir2,file))
        origin=sitk.GetArrayFromImage(origin)
        outo = sitk.GetImageFromArray(origin[i-1,:,:])
        sitk.WriteImage(outo,os.path.join(objDir2,str(a)+'.nii.gz'))
        a+=1
    '''

#SLICE (L/R)
objDir=r"/home/konata/Dataset/TED_MRI/T2/mask/seg_slice_LR/"
objDir2=r"/home/konata/Dataset/TED_MRI/T2/mask/origin_slice_LR/"
if not os.path.exists(objDir):
    os.mkdir(objDir)
if not os.path.exists(objDir2):
    os.mkdir(objDir2)
tbar=tqdm.tqdm(unique.items())
a=1
for item in tbar:
    file=item[0]
    slice=item[1][1]
    
    '''
    seg=sitk.ReadImage(os.path.join(baseDir,file))
    origin=sitk.ReadImage(os.path.join(baseDir2,file))
    spacing=seg.GetSpacing()
    origin=seg.GetOrigin()
    direction=seg.GetDirection()
    size=seg.GetSize()
    '''
    for i in slice:
        seg=sitk.ReadImage(os.path.join(baseDir,file))
        seg=sitk.GetArrayFromImage(seg)
        shape=seg.shape[2]
        outsR = sitk.GetImageFromArray(seg[i-1,:,0:shape//2])
        outsL = sitk.GetImageFromArray(seg[i-1,:,shape//2:shape])
        sitk.WriteImage(outsL,os.path.join(objDir,str(a)+'_L.nii.gz'))
        sitk.WriteImage(outsR,os.path.join(objDir,str(a)+'_R.nii.gz'))

        origin=sitk.ReadImage(os.path.join(baseDir2,file))
        origin=sitk.GetArrayFromImage(origin)
        outoR = sitk.GetImageFromArray(origin[i-1,:,0:shape//2])
        outoL = sitk.GetImageFromArray(origin[i-1,:,shape//2:shape])
        sitk.WriteImage(outoL,os.path.join(objDir2,str(a)+'_L.nii.gz'))
        sitk.WriteImage(outoR,os.path.join(objDir2,str(a)+'_R.nii.gz'))
        a+=1