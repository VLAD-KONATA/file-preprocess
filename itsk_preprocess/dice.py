import torch
import os
import numpy as np
import SimpleITK as sitk

def Dice(pre,gd):
    dice=((pre*gd).sum().item()*2+1e-5)/(pre.sum().item()+gd.sum().item()+1e-5)
    return dice

def soft_dice(pre,gd):
    dice=0
    pre=pre[::2,:,:]
    gd=torch.squeeze(gd).to(device='cuda:0')
    pre=torch.squeeze(pre).to(device='cuda:0')
    A=torch.unique(gd)
    assert pre.shape==gd.shape
    for i in A:
        i=i.item()
        if i!=0:
            pre_=(pre==i).int()
            gd_=(gd==i).int()
            dice+=Dice(pre_,gd_)
    return dice/(len(A)-1)

pre_path='C:/Users\/VLADKONATA/Desktop/receive/seg'
gd_path='C:/Users/VLADKONATA/Desktop/receive/label'
files=os.listdir(pre_path)
dice=0
for file in files:
    label=sitk.ReadImage(os.path.join(gd_path,file))
    seg=sitk.ReadImage(os.path.join(pre_path,file))
    label=sitk.GetArrayFromImage(label)
    seg=sitk.GetArrayFromImage(seg)
    gd=torch.from_numpy(label.astype(float))
    pre=torch.from_numpy(seg.astype(float))
    print(file,soft_dice(pre,gd))
    dice+=soft_dice(pre,gd)
print(f'dicemean={dice/len(files)}')
    