"""
作者：ztf08
名称：连通性.py
说明：分离左右眼
日期：2022/8/11 13:07
"""
import os

import numpy as np
from scipy.ndimage import label
import SimpleITK as sitk


def remove_all_but_the_largest_connected_component(filename,image: np.ndarray, for_which_classes=None, volume_per_voxel=1.0,
                                                   minimum_valid_object_size: dict = None):
    """
    removes all but the largest connected component, individually for each class
    只保留最大联通区域
    :param image:
    :param for_which_classes: can be None. Should be list of int. Can also be something like [(1, 2), 2, 4].
    Here (1, 2) will be treated as a joint region, not individual classes (example LiTS here we can use (1, 2)
    to use all foreground classes together)
    :param minimum_valid_object_size: Only objects larger than minimum_valid_object_size will be removed. Keys in
    minimum_valid_object_size must match entries in for_which_classes
    :return:
        image: 只保留最大联通区域的图像
        largest_removed: 删除的区域大小
        kept_size: 保留的区域大小
        left_right: 0 左眼，1 右眼
    """
    if for_which_classes is None:
        for_which_classes = np.unique(image)
        for_which_classes = for_which_classes[for_which_classes > 0]

    assert 0 not in for_which_classes, "cannot remove background"
    largest_removed = {}
    kept_size = {}
    for c in for_which_classes:
        if isinstance(c, (list, tuple)):  # 判断c是否是list/tuple
            c = tuple(c)  # otherwise it cant be used as key in the dict
            mask = np.zeros_like(image, dtype=bool)
            for cl in c:
                mask[image == cl] = True
        else:
            mask = image == c
        # get labelmap and number of objects
        lmap, num_objects = label(mask.astype(int))
        # 标记联通区域，默认规则4联通，返回标记好的label和联通区域数量

        # collect object sizes
        object_sizes = {}
        for object_id in range(1, num_objects + 1):
            object_sizes[object_id] = (lmap == object_id).sum() * volume_per_voxel

        # 判断左右眼
        object_sizes = sorted(object_sizes.items(),key=lambda x:x[1],reverse=True)
        max_liantong_index = object_sizes[0][0]
        second_liantong_index = object_sizes[1][0]
        if num_objects!=2:
            for i in range(2,len(object_sizes)):
                liantong_index = object_sizes[i][0]
                if abs(min(np.where(lmap == max_liantong_index)[2])-min(np.where(lmap == liantong_index)[2]))<abs(min(np.where(lmap == second_liantong_index)[2]) - min(np.where(lmap == liantong_index)[2])):
                    lmap[lmap==liantong_index]=max_liantong_index
                else:
                    lmap[lmap==liantong_index]=second_liantong_index
        assert len(np.unique(lmap))==3,'!2'
        num_objects = 2

        lmap[lmap==max_liantong_index]=100
        lmap[lmap==second_liantong_index]=200
        lmap[lmap == 100] = 1
        lmap[lmap == 200] = 2

        object_sizes = {}
        for object_id in range(1, num_objects + 1):
            object_sizes[object_id] = (lmap == object_id).sum() * volume_per_voxel

        max_liantong_index=1
        second_liantong_index=2

        if min(np.where(lmap == max_liantong_index)[2]) < min(np.where(lmap == second_liantong_index)[2]):
            # print('右眼')
            left_right = 1
        else:
            # print('左眼')
            left_right = 0

        largest_removed[c] = None
        kept_size[c] = None

        if num_objects > 0:
            # we always keep the largest object. We could also consider removing the largest object if it is smaller
            # than minimum_valid_object_size in the future but we don't do that now.
            maximum_size = max((lmap == 1).sum(),(lmap == 2).sum())
            kept_size[c] = maximum_size

            for object_id in range(1, num_objects + 1):
                # we only remove objects that are not the largest
                if object_sizes[object_id] != maximum_size:
                    # we only remove objects that are smaller than minimum_valid_object_size
                    remove = True
                    if minimum_valid_object_size is not None:
                        remove = object_sizes[object_id] < minimum_valid_object_size[c]
                    if remove:
                        image[(lmap == object_id) & mask] = 0
                        if largest_removed[c] is None:
                            largest_removed[c] = object_sizes[object_id]
                        else:
                            largest_removed[c] = max(largest_removed[c], object_sizes[object_id])
    return image, largest_removed, kept_size, left_right

def remove_minist_connected_component(image: np.ndarray, for_which_classes: list=None, volume_per_voxel: float=None,
                                                   minimum_valid_object_size=100):
    """
    removes all but the largest connected component, individually for each class
    删掉小联通域
    :param image:
    :param for_which_classes: can be None. Should be list of int. Can also be something like [(1, 2), 2, 4].
    Here (1, 2) will be treated as a joint region, not individual classes (example LiTS here we can use (1, 2)
    to use all foreground classes together)
    :param minimum_valid_object_size: Only objects larger than minimum_valid_object_size will be removed. Keys in
    minimum_valid_object_size must match entries in for_which_classes
    :return:
        image: 删掉小联通区域的图像
    """
    if for_which_classes is None:
        for_which_classes = np.unique(image)
        for_which_classes = for_which_classes[for_which_classes > 0]

    assert 0 not in for_which_classes, "cannot remove background"
    remove_mask = np.ones_like(image)
    for c in for_which_classes:
        if isinstance(c, (list, tuple)):  # 判断c是否是list/tuple
            c = tuple(c)  # otherwise it cant be used as key in the dict
            mask = np.zeros_like(image, dtype=bool)
            for cl in c:
                mask[image == cl] = True
        else:
            mask = image == c
        # get labelmap and number of objects
        lmap, num_objects = label(mask.astype(int))
        # 标记联通区域，默认规则4联通，返回标记好的label和联通区域数量

        if num_objects > 2:
            object_sizes = {}
            for object_id in range(1, num_objects + 1):
                object_sizes[object_id] = (lmap == object_id).sum() * volume_per_voxel
            object_sizes = dict(sorted(object_sizes.items(),key=lambda x:x[1], reverse=True))
            remove_num = list(object_sizes.keys())[2:]
            for num in remove_num:
                remove_mask[lmap==num]=0
    image = image*remove_mask
    a = np.mean(image, axis=0)
    #if(len(image.shape)>2):
    #   a = np.mean(a, axis=0)
    a = np.array(np.nonzero(a)).reshape(-1)
    split_indices = np.where(np.diff(a) != 1)[0] + 1  # 找到不连续的位置
    sub_arrays = np.split(a, split_indices)
    mid = (sub_arrays[1][0]-sub_arrays[0][1])


    return image,mid


def set_image(img_out, img_ori):
    img_out.SetOrigin(img_ori.GetOrigin())
    img_out.SetDirection(img_ori.GetDirection())
    img_out.SetSpacing(img_ori.GetSpacing())
    return img_out

def main():
    root_dir = '/media/dell/SATA1/dataset/MRI/T1C/seg_cut_unpp/'
    save_dir = '/media/dell/SATA1/dataset/MRI/T1C/seg_cut_unpp/'
    # save_dir = '/media/dell/SATA1/dataset/MRI/T1/left_right/seg'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    filename = os.listdir(root_dir)
    error=['1056_2020-11-27.nii.gz','430_2019-04-09.nii.gz','788_2020-08-14.nii.gz','983_2020-11-20.nii.gz']
    i=0
    for file in filename:
        # try:
            i+=1
            print(i,'/',len(filename))
            seg_path = root_dir+file
            origin_path = seg_path.replace('seg_cut_unet','origin_cut')
            vol_ori=sitk.ReadImage(origin_path)
            origin_img = sitk.GetArrayFromImage(vol_ori)
            img0 = sitk.ReadImage(seg_path)
            img = sitk.GetArrayFromImage(img0)
            image,mid = remove_minist_connected_component(img,volume_per_voxel=1.0, minimum_valid_object_size=100)

            # 保存整张图
            outlabelmapraw = sitk.GetImageFromArray(image.astype(np.uint8))
            outlabelmapraw.SetDirection(vol_ori.GetDirection())
            outlabelmapraw.SetSpacing(vol_ori.GetSpacing())
            outlabelmapraw.SetOrigin(vol_ori.GetOrigin())
            sitk.WriteImage(outlabelmapraw, os.path.join(save_dir, file))

            # 分左右眼保存
            # right_image = origin_img[:, :, 0:mid]
            # left_image = origin_img[:, :, mid:]
            # left_image = sitk.GetImageFromArray(left_image)
            # right_image = sitk.GetImageFromArray(right_image)
            # right_image = set_image(right_image,img0)
            # left_image = set_image(left_image,img0)
            # sitk.WriteImage(right_image,
            #                 os.path.join(save_dir, file.split('.')[0]+'_r.nii.gz'))
            # sitk.WriteImage(left_image,
            #                 os.path.join(save_dir, file.split('.')[0]+'_l.nii.gz'))

            # image, largest_removed, kept_size, left_right = remove_all_but_the_largest_connected_component(file,img, volume_per_voxel=1.0, minimum_valid_object_size=None)
            # if left_right == 0:
            #     image_left = image
            #     image_right = img1 - image
            # else:
            #     image_left = img1 - image
            #     image_right = image
            #
            # img_out_left = sitk.GetImageFromArray(image_left)
            # img_out_left = set_image(img_out_left, img0)
            # sitk.WriteImage(img_out_left, save_dir_left+file)
            #
            # img_out_right = sitk.GetImageFromArray(image_right)
            # img_out_right = set_image(img_out_right, img0)
            # sitk.WriteImage(img_out_right, save_dir_right+file)
        # except:
        #     print(file)

