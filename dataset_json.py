import copy
import glob
import os
import re
import json
from collections import OrderedDict

#####下面是创建json文件的内容
#可以根据你的数据集，修改里面的描述
json_dict = OrderedDict()
json_dict['dataset_name'] = 'TOM500'
baseDir='/home/konata/Dataset/TED_MRI/TOM500/slice/val'
seq_list=[]
seq_info=[]
folders=os.listdir(baseDir)
for folder in folders:
    seq_list.clear()
    files=os.listdir(os.path.join(baseDir,folder))
    seq_len=len(files)
    for i in range(seq_len):
        seq_dir=os.path.join(baseDir,folder,str(i)+'.png')
        seq_list.append(seq_dir)
    seq_info.append({"seq_list":copy.deepcopy(seq_list),"seq_len":seq_len})

json_dict['seq_info'] = seq_info
json_dict['size'] = len(folders)


with open(os.path.join('/home/konata/Git/VFI/data_description', "TOM500_dataset_val.json"), 'w') as f:
    json.dump(json_dict, f, indent=4, sort_keys=True)
