# D:/Git/TAO_MRI/feature-2D/data/T2(T1)(T1C)/origin(mask)
import SimpleITK as sitk
import nibabel
import os
import numpy as np
from tqdm import tqdm
#image_array = nibabel.load("D:/Git/TAO_MRI/feature-2D/seg/seg/1_2018-04-12.nii.gz").get_fdata()



def slice(modality):   
    origin_path=r'D:/data/TAO_MRI/'+modality+'/origin/'
    mask_path=r'D:/data/TAO_MRI/'+modality+'/seg_unpp/'
    image_list=os.listdir(origin_path)
    image_list.sort(key=(lambda x: int(x.split('_')[0])))
    
    slice_list=[]
    for image_name in tqdm(image_list):
        try:
            if not os.path.exists(r'D:/Git/TAO_MRI/feature-2D/data/'+modality+'/mask/'+image_name):
                os.makedirs(r'D:/Git/TAO_MRI/feature-2D/data/'+modality+'/mask/'+image_name)
            mask = sitk.ReadImage(mask_path+image_name)
            datam = sitk.GetArrayFromImage(mask)
            for i in range(datam.shape[0]):
                mask_slice=datam[i,:,:]
                if(np.any(mask_slice)==True):
                    slice_list.append(i)
                    mslice_name = r'D:/Git/TAO_MRI/feature-2D/data/'+modality+'/mask/'+image_name+'/'+str(len(slice_list))+'.nii.gz'
                    out = sitk.GetImageFromArray(mask_slice)
                    out1 = sitk.WriteImage(out,mslice_name)
                
            if not os.path.exists(r'D:/Git/TAO_MRI/feature-2D/data/'+modality+'/origin/'+image_name):
                os.makedirs(r'D:/Git/TAO_MRI/feature-2D/data/'+modality+'/origin/'+image_name)
            origin = sitk.ReadImage(origin_path+image_name)
            datao = sitk.GetArrayFromImage(origin)
            for i in range(datao.shape[0]):
                origin_slice=datao[i,:,:]
                if i in slice_list:
                    oslice_name = r'D:/Git/TAO_MRI/feature-2D/data/'+modality+'/origin/'+image_name+'/'+str(slice_list.index(i)+1)+'.nii.gz'
                    out = sitk.GetImageFromArray(origin_slice)
                    out1 = sitk.WriteImage(out,oslice_name)
        
            slice_list.clear()
        except:
            print('\nerror_name:',image_name)
            with open(r'feature-2D/'+modality+'_error_log.txt','a') as file:
                file.write(image_name+'\n')
            if os.path.exists(r'D:/Git/TAO_MRI/feature-2D/data/'+modality+'/mask/'+image_name):
                os.removedirs(r'D:/Git/TAO_MRI/feature-2D/data/'+modality+'/mask/'+image_name)
            if os.path.exists(r'D:/Git/TAO_MRI/feature-2D/data/'+modality+'/origin/'+image_name):
                os.removedirs(r'D:/Git/TAO_MRI/feature-2D/data/'+modality+'/origin/'+image_name)
            slice_list.clear()
            continue
    
if __name__ == '__main__':
    modality_list=['T1','T2','T1C']
    modality=modality_list[2]
    
    with open(r'feature-2D/'+modality+'_error_log.txt','a') as file:
        file.write('error_name:\n')
    slice(modality)
