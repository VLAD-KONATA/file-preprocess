import torch
from torch.utils.data import Dataset
from torchvision import transforms
import SimpleITK as sitk
from scipy import ndimage
import numpy as np
import random

@staticmethod
def normalize(data):
    data = data.astype(np.float32)
    data = (data - np.min(data)) / (np.max(data) - np.min(data))
    return data

def get_index(slices):
        indexs=[]
        max=0
        for i in slices:
            if len(np.unique(i))>max:
                max=len(np.unique(i))
        for i in range(len(slices)):
            if len(np.unique(slices[i]))==max:
                indexs.append(i)
        if len(indexs)==1:
            return indexs[0]
        elif len(indexs)%2==0:
            return indexs[(len(indexs)//2)-1]
        else:
            return indexs[(len(indexs)//2)]
        
def random_rotate(image, seg):
    angle = np.random.randint(-20, 20)
    image = ndimage.rotate(image, angle, order=0, reshape=False)
    seg = ndimage.rotate(seg, angle, order=0, reshape=False)
    return image, seg

class TrainSet3D(Dataset):
    def __init__(self,data_list,origin_path,seg_path,transform=None):
        self.data_list=data_list
        self.origin_path=origin_path
        self.seg_path=seg_path
        self.transform=transform

    def __getitem__(self,item):
        id=self.data_list['id'][item]

        ori_raw=sitk.ReadImage(self.origin_path+'/'+id)
        ori_img=sitk.GetArrayFromImage(ori_raw)

        #   try:labeled img  |  except:unlabeled img
        try:
            seg_raw=sitk.ReadImage(self.seg_path+'/'+id)
            seg_img=sitk.GetArrayFromImage(seg_raw)
        except:
            seg_img=np.zeros_like(ori_img).astype(float)

        #   图像标准化 从ori_img减去像素均值并除以像素值的标准差，使像素值标准化到均值为0，标准差为1
        norm_ori_img=(ori_img-np.mean(ori_img))/np.std(ori_img)
        '''
        # 在类别标签不为0/1时（即不是背景or前景），对图像进行随机增强：
        label = self.data_list['label'][item]
        if label not in [0,1]:
            #   转化为张量，且在第二维增加一个维度（以符合后续torchvision函数的输入格式要求，BCDHW，D为3d图像特供）
            ori_img = torch.tensor(norm_ori_img).unsqueeze(1)
            if random.random() < 0.8:
                #   80%概率将该图像增强鲜艳度，对比度，亮度，饱和度
                ori_img = transforms.ColorJitter(0.5, 0.5, 0.5, 0.5)(ori_img)
            if random.random() < 0.5:
                #   50%概率将该图像高斯模糊，sigma为高斯核的标准差，在(0.1,2.0)范围中随机选取
                sigma = np.random.uniform(0.1, 2.0)
                ori_img = transforms.GaussianBlur(kernel_size=3,sigma=sigma)(ori_img)
            #   降维，去除多余维度（之前unsqueeze的维度）并转换为numpy数组
            ori_img = torch.squeeze(ori_img).numpy()
        #   再次标准化处理，防止颜色增强和高斯模糊改变了图像的像素值分布
        norm_ori_img = (ori_img - np.mean(ori_img)) / np.std(ori_img)
        '''
        #T1 模态共有 6 类分割标签,分别为眼球、视神经、上直肌、下直肌、内直肌和外直肌;
        #T2 模态有 8 类分割标签,分别为视神经、上直肌、下直肌、内直肌、外直肌、脂肪、泪腺、上斜肌;
        #T1C模态有 6 类分割标签,分别为上直肌、下直肌、内直肌、外直肌、泪腺、上斜肌。
        '''
        if len(np.unique(label))==7:
            label[label==7]=5
            label[label==8]=6
        '''
        sample = {'image':norm_ori_img, 'seg': seg_img}
        if self.transform:
            sample = self.transform(sample)
        return sample  

    
    def __len__(self):
        return len(self.data_list)
    
class TrainSet2D(Dataset):
    def __init__(self, data_list, origin_path,seg_path):
        self.data_list=data_list
        self.origin_path=origin_path
        self.seg_path=seg_path

    def __getitem__(self, item):
        id = self.data_list['id'][item]

        ori_raw=sitk.ReadImage(self.origin_path+'/'+id)
        ori_img=sitk.GetArrayFromImage(ori_raw)

        norm_ori_img=(ori_img-np.mean(ori_img))/np.std(ori_img)

        data_tensor = torch.from_numpy(norm_ori_img).float()
        data_tensor = torch.unsqueeze(data_tensor,dim=0)

        seg_raw=sitk.ReadImage(self.seg_path+'/'+id)
        seg_img=sitk.GetArrayFromImage(seg_raw)
        seg_img = torch.from_numpy(seg_img.astype(float))
        return id, data_tensor,seg_img # 遍历一次，拿到的数据是怎么样的？
    
    def __len__(self):
        return len(self.data_list) 

class ValSet3D(Dataset):

    def __init__(self,data_list,origin_path,seg_path):
        self.data_list=data_list
        self.origin_path=origin_path
        self.seg_path=seg_path


    def __getitem__(self, item):
        id = self.data_list['id'][item]

        preimgraw = sitk.ReadImage(self.origin_path + "/" +id)
        preimg = sitk.GetArrayFromImage(preimgraw)
        labelraw = sitk.ReadImage(self.seg_path + "/" +id)
        label_seg = sitk.GetArrayFromImage(labelraw).astype(float)
        if len(np.unique(label_seg))==7:
            label_seg[label_seg==7]=5
            label_seg[label_seg==8]=6
        normpreimg = (preimg - np.mean(preimg)) / np.std(preimg)
        data_tensor = torch.from_numpy(normpreimg).float()
        data_tensor = torch.unsqueeze(data_tensor,dim=0)

        return id,data_tensor, label_seg # 遍历一次，拿到的数据是怎么样的？

    @staticmethod
    def normalize(data):
        data = data.astype(np.float32)
        data = (data - np.min(data)) / (np.max(data) - np.min(data))
        return data

    def __len__(self):
        return len(self.data_list)

class TestSet3D(Dataset):

    def __init__(self, data_list, origin_path,seg_path):
        self.data_list = data_list
        self. origin_path =  origin_path
        self.seg_path=seg_path

    def __getitem__(self, item):
        id = self.data_list['id'][item]

        preimgraw = sitk.ReadImage(self. origin_path + "/" +id)
        preimg = sitk.GetArrayFromImage(preimgraw)
        normpreimg = (preimg - np.mean(preimg)) / np.std(preimg)
        data_tensor = torch.from_numpy(normpreimg).float()
        data_tensor = torch.unsqueeze(data_tensor,dim=0)
        seg_raw=sitk.ReadImage(self.seg_path+'/'+id)
        seg_img=sitk.GetArrayFromImage(seg_raw)
        seg = torch.from_numpy(seg_img.astype(float))
        return id,data_tensor,seg # 遍历一次，拿到的数据是怎么样的？

    @staticmethod
    def normalize(data):
        data = data.astype(np.float32)
        data = (data - np.min(data)) / (np.max(data) - np.min(data))
        return data

    def __len__(self):
        return len(self.data_list)
class RandomCrop3D(object):
    """
    Crop randomly the image in a sample
    Args:
    output_size (int): Desired output size
    """

    def __init__(self, output_size, with_sdf=False):
        self.output_size = output_size
        self.with_sdf = with_sdf

    def __call__(self, sample):
        image, seg = sample['image'], sample['seg']
        sample_num = 0
        patchdims = self.output_size
        slice_, height_, width_ = image.shape

        if seg.sum() != 0:
            maxv = np.zeros((3, 1))
            minv = np.zeros((3, 1))  # 存放index每列最大最小值
            index = np.argwhere(seg > 0)
            for ii in range(0, 3):
                maxv[ii] = np.max(index[:, ii])
                minv[ii] = np.min(index[:, ii])
            while sample_num < 100:
                z_min = np.random.randint(max(minv[0][0] - int(patchdims[0] / 2) + 1, int(patchdims[0] / 2)),
                                          min(maxv[0][0] + int(patchdims[0] / 2) - 1,
                                              slice_ - int(patchdims[0] / 2) + 1))
                y_min = np.random.randint(max(minv[1][0] - int(patchdims[1] / 2) + 10, int(patchdims[1] / 2)),
                                          min(maxv[1][0] + int(patchdims[1] / 2) - 10,
                                              height_ - int(patchdims[1] / 2) + 1))
                x_min = np.random.randint(max(minv[2][0] - int(patchdims[2] / 2) + 10, int(patchdims[2] / 2)),
                                          min(maxv[2][0] + int(patchdims[2] / 2) - 10,
                                              width_ - int(patchdims[2] / 2) + 1))

                z0 = z_min - int(patchdims[0] / 2)
                z1 = z_min + int(patchdims[0] / 2)
                y0 = y_min - int(patchdims[1] / 2)
                y1 = y_min + int(patchdims[1] / 2)
                x0 = x_min - int(patchdims[2] / 2)
                x1 = x_min + int(patchdims[2] / 2)

                image0 = image[z0:z1, y0:y1, x0:x1]
                seg0 = seg[z0:z1, y0:y1, x0:x1]
                sample_num += 1
                if seg0.sum() > 1000:
                    break
        else:
            z0 = int(np.random.randint(0, slice_ - self.output_size[0]+1))
            z1 = int(z0 + self.output_size[0])
            y0 = int(np.random.randint(0, height_ - self.output_size[1]+1))
            y1 = int(y0 + self.output_size[1])
            x0 = int(np.random.randint(0, width_ - self.output_size[2]+1))
            x1 = int(x0 + self.output_size[2])

            image0 = image[z0:z1, y0:y1, x0:x1]
            seg0 = seg[z0:z1, y0:y1, x0:x1]

        return {'image': image0, 'seg': seg0}

class RandomCrop2D(object):
    """
    Crop randomly the image in a sample
    Args:
    output_size (int): Desired output size
    """

    def __init__(self, output_size, with_sdf=False):
        self.output_size = output_size
        self.with_sdf = with_sdf

    def __call__(self, sample):
        id,image, seg =sample['name'], sample['image'], sample['seg']
        sample_num = 0
        patchdims = self.output_size
        height_, width_ =image[0].shape

        if seg.sum() != 0:
            maxv = np.zeros((2, 1))
            minv = np.zeros((2, 1))  # 存放index每列最大最小值
            index = np.argwhere(seg > 0)
            for ii in range(0, 2):
                maxv[ii] = np.max(index[:, ii])
                minv[ii] = np.min(index[:, ii])
            while sample_num < 100:
                y_min = np.random.randint(max(minv[0][0] - int(patchdims[0] / 2) + 10, int(patchdims[0] / 2)),
                                          min(maxv[0][0] + int(patchdims[0] / 2) - 10,
                                              height_ - int(patchdims[0] / 2) + 1))
                x_min = np.random.randint(max(minv[1][0] - int(patchdims[1] / 2) + 10, int(patchdims[1] / 2)),
                                          min(maxv[1][0] + int(patchdims[1] / 2) - 10,
                                              width_ - int(patchdims[1] / 2) + 1))

               
                y0 = y_min - int(patchdims[0] / 2)
                y1 = y_min + int(patchdims[0] / 2)
                x0 = x_min - int(patchdims[1] / 2)
                x1 = x_min + int(patchdims[1] / 2)

                image0 = image[y0:y1, x0:x1]
                seg0 = seg[y0:y1, x0:x1]
                sample_num += 1
                if seg0.sum() > 1000:
                    break
        else:
            y0 = int(np.random.randint(0, height_ - self.output_size[0]+1))
            y1 = int(y0 + self.output_size[0])
            x0 = int(np.random.randint(0, width_ - self.output_size[1]+1))
            x1 = int(x0 + self.output_size[1])

            image0 = image[y0:y1, x0:x1]
            seg0 = seg[ y0:y1, x0:x1]

        return {'name':id,'image': image0, 'seg': seg0}
    
class Padding_img3D(object):
    def __init__(self,output_size):
            self.size=output_size
        
    def __call__(self,sample):
        image, seg = sample['image'], sample['seg']
        df_v = self.size-np.array(image.shape)
        df_v[df_v<0]=0
        image = np.pad(image,[[df_v[0]//2,df_v[0]-df_v[0]//2],[df_v[1]//2,df_v[1]-df_v[1]//2],
                          [df_v[2]//2,df_v[2]-df_v[2]//2]],
                     mode='constant')
        seg = np.pad(seg,[[df_v[0]//2,df_v[0]-df_v[0]//2],[df_v[1]//2,df_v[1]-df_v[1]//2],
                          [df_v[2]//2,df_v[2]-df_v[2]//2]],
                     mode='constant')
        return {'image': image, 'seg': seg}
    
'''
Crop randomly flip the dataset in a sample
Args:
output_size (int): Desired output size
'''
class RandomRot(object):
    def __call__(self, sample):
        image, seg = sample['image'], sample['seg']
        image, seg = random_rotate(image, seg)

        return {'image': image, 'seg': seg}

'''
Convert ndarrays in sample to Tensors.
'''
class ToTensor3D(object):
    def __call__(self, sample):
        image = sample['image']
        seg = sample['seg'].astype(np.uint8)
        image = image.reshape(1, image.shape[0], image.shape[1], image.shape[2]).astype(np.float32)
        num_classes=9
        onehot_label = np.zeros((num_classes, seg.shape[0], seg.shape[1],seg.shape[2]), dtype=np.float32)
        for i in range(num_classes):
            onehot_label[i, :, :,:] = (seg == i).astype(np.float32)
        #seg = seg.reshape(1, seg.shape[0], seg.shape[1], seg.shape[2])
        #return {'image': torch.from_numpy(image), 'seg': torch.from_numpy(seg).long()}
        return {'image': torch.from_numpy(image), 'seg': torch.from_numpy(onehot_label)}

class ToTensor2D(object):
    def __call__(self, sample):
        id=sample['name']
        image = sample['image']
        image = image.reshape(1, image.shape[0], image.shape[1]).astype(np.float32)
        seg = sample['seg'].astype(np.uint8)
        num_classes=9
        onehot_label = np.zeros((num_classes, seg.shape[0], seg.shape[1]), dtype=np.float32)
        for i in range(num_classes):
            onehot_label[i, :, :] = (seg == i).astype(np.float32)
        #seg = seg.reshape(1, seg.shape[0], seg.shape[1])
        return {'name':id,'image': torch.from_numpy(image), 'seg': torch.from_numpy(onehot_label)}
