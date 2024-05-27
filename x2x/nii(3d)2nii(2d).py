{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import SimpleITK as sitk\n",
    "import numpy\n",
    "import json"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'637_2020-05-11.nii.gz': [9, [6]], '683_2020-06-16.nii.gz': [9, [6, 7]], '430_2019-04-09.nii.gz': [9, [6, 7]], '681_2020-06-12.nii.gz': [9, [4, 5, 6]], '440_2018-11-29.nii.gz': [9, [6]], '1656_2021-05-13.nii.gz': [8, [8, 9, 10]], '36_2019-05-09.nii.gz': [9, [6, 7, 8]], '740_2020-07-13.nii.gz': [9, [6, 7]], '886_2020-08-06.nii.gz': [9, [7, 8]], '1142_2021-03-04.nii.gz': [9, [5, 6]], '516_2018-02-13.nii.gz': [9, [6]], '199_2019-05-16.nii.gz': [9, [7]], '1265_2021-05-07.nii.gz': [9, [6]], '748_2020-08-03.nii.gz': [9, [6, 7]], '482_2018-11-08.nii.gz': [9, [7]], '460_2017-10-20.nii.gz': [9, [6, 7]], '1645_2021-05-15.nii.gz': [9, [7, 8]], '495_2019-06-18.nii.gz': [9, [5, 6]], '788_2020-08-14.nii.gz': [9, [6, 7, 8]], '976_2020-11-13.nii.gz': [9, [5, 6]], '1247_2021-02-19.nii.gz': [9, [6, 7]], '1248_2021-05-04.nii.gz': [9, [6, 7]], '570_2018-05-30.nii.gz': [9, [6]], '1520_2021-05-30.nii.gz': [9, [5, 6, 7, 8]], '1015_2021-03-23.nii.gz': [9, [5, 6]], '1630_2021-05-11.nii.gz': [9, [5]], '522_2019-01-30.nii.gz': [9, [4]], '162_2019-08-15.nii.gz': [9, [4]], '391_2018-02-08.nii.gz': [9, [7]], '1477_2021-09-18.nii.gz': [9, [6]], '198_2019-11-20.nii.gz': [9, [6, 7]], '1668_2021-06-26.nii.gz': [9, [7]], '984_2020-11-19.nii.gz': [9, [6, 7]], '653_2019-12-04.nii.gz': [9, [5, 6]], '452_2018-11-20.nii.gz': [9, [6, 7]], '443_2019-03-21.nii.gz': [9, [6, 7]], '336_2020-03-26.nii.gz': [9, [6]], '127_2019-09-04.nii.gz': [8, [4, 6, 7, 8, 9, 10, 11, 12]], '673_2020-06-05.nii.gz': [8, [6, 7, 8, 9, 10, 11, 12]], '1093_2021-02-09.nii.gz': [9, [6]], '191_2019-11-20.nii.gz': [9, [6, 7]], '992_2020-11-12.nii.gz': [9, [6, 7]], '1657_2021-07-06.nii.gz': [9, [6]], '1385_2021-06-28.nii.gz': [9, [6]], '465_2018-02-26.nii.gz': [9, [5, 6]], '1186_2021-03-27.nii.gz': [9, [5, 6, 7, 8]], '1092_2021-02-09.nii.gz': [8, [3, 4, 5, 6, 7, 8, 9, 10]], '699_2020-07-07.nii.gz': [9, [7]], '134_2019-10-08.nii.gz': [9, [6, 7]], '908_2020-03-26.nii.gz': [9, [7]], '816_2020-08-20.nii.gz': [9, [6, 7]], '1315_2021-05-30.nii.gz': [9, [6, 7]], '648_2020-05-27.nii.gz': [8, [5, 6, 7, 8, 9, 10, 11]], '1303_2021-05-30.nii.gz': [9, [6, 7]], '423_2018-10-23.nii.gz': [9, [6, 7]], '973_2020-04-15.nii.gz': [9, [5, 6, 7]], '1053_2019-04-18.nii.gz': [9, [6, 7]], '106_2019-09-20.nii.gz': [9, [5, 6, 7]], '1073_2020-11-26.nii.gz': [9, [5, 6, 7]], '66_2019-08-15.nii.gz': [9, [6]], '812_2021-04-01.nii.gz': [9, [5, 6, 7, 8]], '1571_2021-09-04.nii.gz': [9, [7, 8]], '1131_2021-03-18.nii.gz': [9, [7, 8]], '224_2019-11-26.nii.gz': [9, [5, 6]], '789_2020-08-17.nii.gz': [9, [6, 7]], '888_2020-10-08.nii.gz': [9, [6, 7, 8, 9]], '1527_2018-07-27.nii.gz': [9, [6]], '426_2019-04-16.nii.gz': [9, [7, 8]], '517_2018-01-26.nii.gz': [9, [7, 8]], '1525_2018-03-02.nii.gz': [9, [5, 6, 7]], '315_2019-07-19.nii.gz': [9, [5, 6]], '630_2020-05-18.nii.gz': [9, [7]], '88_2019-09-18.nii.gz': [9, [8, 9]], '1314_2021-06-02.nii.gz': [9, [5, 6, 7, 8]], '719_2020-07-08.nii.gz': [9, [7, 8]], '930_2020-10-24.nii.gz': [9, [6, 7, 8]], '1255_2020-10-29.nii.gz': [9, [7, 8]], '1241_2021-04-28.nii.gz': [9, [6]], '568_2019-02-28.nii.gz': [9, [7, 8, 9]], '1280_2021-05-11.nii.gz': [9, [6, 7]], '829_2020-09-04.nii.gz': [8, [5, 6, 7, 8, 9]], '1014_2020-12-17.nii.gz': [8, [6, 7, 8, 9, 10, 11]], '1422_2021-05-11.nii.gz': [9, [6, 7]], '1313_2021-06-10.nii.gz': [9, [5, 6, 7]], '41_2019-05-17.nii.gz': [9, [6]], '833_2020-09-04.nii.gz': [9, [5]], '706_2020-06-29.nii.gz': [9, [4, 5, 6, 7]], '944_2020-11-04.nii.gz': [9, [5, 6, 7]], '613_2020-05-04.nii.gz': [9, [7]], '360_2020-04-16.nii.gz': [9, [5, 6]], '435_2019-02-14.nii.gz': [9, [5, 6]], '1367_2021-06-16.nii.gz': [9, [6, 7, 8]], '883_2020-09-23.nii.gz': [9, [5, 6, 7]], '1585_2021-11-01.nii.gz': [9, [5, 6]], '1031_2020-11-19.nii.gz': [8, [3, 4, 6, 7, 8, 9, 10]], '1095_2021-01-21.nii.gz': [9, [7, 8]], '1541_2018-01-11.nii.gz': [9, [6, 7]], '493_2018-06-21.nii.gz': [8, [5, 6, 7, 8, 9, 10, 11]], '1180_2021-03-26.nii.gz': [9, [6, 7, 8]], '124_2019-09-25.nii.gz': [9, [5, 6]], '1644_2021-05-31.nii.gz': [9, [7, 8]], '697_2020-07-06.nii.gz': [9, [5, 6, 7, 8]], '983_2020-11-20.nii.gz': [9, [5]], '998_2020-12-04.nii.gz': [8, [5, 6, 7, 8, 9, 10]], '215_2019-11-20.nii.gz': [9, [6, 7]], '575_2018-07-11.nii.gz': [9, [6, 7, 8]], '904_2020-08-20.nii.gz': [9, [6]], '747_2020-12-02.nii.gz': [9, [6]], '1056_2020-11-27.nii.gz': [9, [6, 7]], '264_2019-11-28.nii.gz': [9, [6]], '680_2020-04-08.nii.gz': [9, [4, 5]], '715_2020-07-03.nii.gz': [9, [6]], '429_2019-04-29.nii.gz': [9, [4, 5]], '332_2020-03-18.nii.gz': [9, [6, 7]], '428_2019-02-19.nii.gz': [9, [6, 7]], '156_2019-10-29.nii.gz': [9, [5, 6]], '1225_2021-04-20.nii.gz': [9, [6, 7]], '1366_2021-06-22.nii.gz': [9, [6, 7, 8]], '1182_2021-03-24.nii.gz': [9, [7, 8, 9]], '1007_2020-12-05.nii.gz': [9, [5, 6]], '593_2018-06-12.nii.gz': [8, [5, 6, 7, 8, 9, 10, 11]], '26_2019-04-04.nii.gz': [9, [6]], '1_2018-04-12.nii.gz': [9, [6, 7]], '709_2020-03-20.nii.gz': [9, [6, 7]], '1257_2021-05-06.nii.gz': [9, [5, 6, 7]], '154_2019-10-10.nii.gz': [9, [6]]}\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "115"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "baseDir = r\"/home/konata/Dataset/TED_MRI/T2/mask/seg_cut/\"\n",
    "baseDir2 = r\"/home/konata/Dataset/TED_MRI/T2/mask/origin_cut/\"\n",
    "objDir=r\"/home/konata/Dataset/TED_MRI/T2/mask/seg_slice/\"\n",
    "objDir2=r\"/home/konata/Dataset/TED_MRI/T2/mask/origin_slice/\"\n",
    "if not os.path.exists(objDir):\n",
    "    os.mkdir(objDir)\n",
    "if not os.path.exists(objDir2):\n",
    "    os.mkdir(objDir2)\n",
    "\n",
    "with open('/home/konata/Dataset/TED_MRI/T2/mask/seg_unique.json', 'r') as file:\n",
    "    unique=json.load(file)\n",
    "print(unique)\n",
    "\n",
    "list8=[]\n",
    "for i in unique.items():\n",
    "    if i[1][0]!=9:\n",
    "          list8.append(i[0])\n",
    "for i in list8:\n",
    "    unique.pop(i)\n",
    "len(unique)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "ename": "TypeError",
     "evalue": "Wrong number or type of arguments for overloaded function 'ImageFileWriter_Execute'.\n  Possible C/C++ prototypes are:\n    itk::simple::ImageFileWriter::Execute(itk::simple::Image const &)\n    itk::simple::ImageFileWriter::Execute(itk::simple::Image const &,std::string const &,bool,int)\n",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mTypeError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m/tmp/ipykernel_6007/2966670978.py\u001b[0m in \u001b[0;36m?\u001b[0;34m()\u001b[0m\n\u001b[1;32m     11\u001b[0m     \u001b[0mseg\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0msitk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mGetArrayFromImage\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mseg\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     12\u001b[0m     \u001b[0morigin\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0msitk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mReadImage\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mos\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mjoin\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mbaseDir2\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mfile\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     13\u001b[0m     \u001b[0morigin\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0msitk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mGetArrayFromImage\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0morigin\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     14\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 15\u001b[0;31m     \u001b[0ms\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0msitk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mWriteImage\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mseg\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mi\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mos\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mjoin\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mobjDir\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mfile\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     16\u001b[0m     \u001b[0mori\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0msitk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mWriteImage\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0morigin\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mi\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mos\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mjoin\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mobjDir2\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mfile\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     17\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m~/anaconda3/envs/preprocess/lib/python3.9/site-packages/SimpleITK/extra.py\u001b[0m in \u001b[0;36m?\u001b[0;34m(image, fileName, useCompression, compressionLevel, imageIO, compressor)\u001b[0m\n\u001b[1;32m    421\u001b[0m     \u001b[0mwriter\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mSetUseCompression\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0museCompression\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    422\u001b[0m     \u001b[0mwriter\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mSetCompressionLevel\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcompressionLevel\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    423\u001b[0m     \u001b[0mwriter\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mSetImageIO\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mimageIO\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    424\u001b[0m     \u001b[0mwriter\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mSetCompressor\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcompressor\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 425\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0mwriter\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mExecute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mimage\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;32m~/anaconda3/envs/preprocess/lib/python3.9/site-packages/SimpleITK/SimpleITK.py\u001b[0m in \u001b[0;36m?\u001b[0;34m(self, *args)\u001b[0m\n\u001b[1;32m   7903\u001b[0m         \u001b[0mExecute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mImageFileWriter\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mImage\u001b[0m \u001b[0marg2\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mstd\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0mstring\u001b[0m \u001b[0mconst\u001b[0m \u001b[0;34m&\u001b[0m \u001b[0minFileName\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mbool\u001b[0m \u001b[0museCompression\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mint\u001b[0m \u001b[0mcompressionLevel\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   7904\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   7905\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   7906\u001b[0m         \"\"\"\n\u001b[0;32m-> 7907\u001b[0;31m         \u001b[0;32mreturn\u001b[0m \u001b[0m_SimpleITK\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mImageFileWriter_Execute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m*\u001b[0m\u001b[0margs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;31mTypeError\u001b[0m: Wrong number or type of arguments for overloaded function 'ImageFileWriter_Execute'.\n  Possible C/C++ prototypes are:\n    itk::simple::ImageFileWriter::Execute(itk::simple::Image const &)\n    itk::simple::ImageFileWriter::Execute(itk::simple::Image const &,std::string const &,bool,int)\n"
     ]
    }
   ],
   "source": [
    "for item in unique.items():\n",
    "    file=item[0]\n",
    "    slice=item[1][1]\n",
    "    if len(slice)>1 and len(slice)%2==1:\n",
    "        i=slice[int(len(slice)/2)]\n",
    "    elif len(slice)>1 and len(slice)%2==0:\n",
    "        i=slice[int(len(slice)/2)-1]\n",
    "    else:\n",
    "        i=slice[0]\n",
    "    seg=sitk.ReadImage(os.path.join(baseDir,file))\n",
    "    seg=sitk.GetArrayFromImage(seg)\n",
    "    origin=sitk.ReadImage(os.path.join(baseDir2,file))\n",
    "    origin=sitk.GetArrayFromImage(origin)\n",
    "    \n",
    "    s=sitk.WriteImage(seg[i,:,:],os.path.join(objDir,file))\n",
    "    ori=sitk.WriteImage(origin[i,:,:],os.path.join(objDir2,file))\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "ename": "TypeError",
     "evalue": "Wrong number or type of arguments for overloaded function 'ImageFileWriter_Execute'.\n  Possible C/C++ prototypes are:\n    itk::simple::ImageFileWriter::Execute(itk::simple::Image const &)\n    itk::simple::ImageFileWriter::Execute(itk::simple::Image const &,std::string const &,bool,int)\n",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n",
      "\u001b[0;31mTypeError\u001b[0m                                 Traceback (most recent call last)\n",
      "\u001b[0;32m/tmp/ipykernel_6007/2966670978.py\u001b[0m in \u001b[0;36m?\u001b[0;34m()\u001b[0m\n",
      "\u001b[1;32m     11\u001b[0m     \u001b[0mseg\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0msitk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mGetArrayFromImage\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mseg\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m     12\u001b[0m     \u001b[0morigin\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0msitk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mReadImage\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mos\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mjoin\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mbaseDir2\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mfile\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m     13\u001b[0m     \u001b[0morigin\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0msitk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mGetArrayFromImage\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0morigin\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m     14\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m---> 15\u001b[0;31m     \u001b[0ms\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0msitk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mWriteImage\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mseg\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mi\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mos\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mjoin\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mobjDir\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mfile\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0m\u001b[1;32m     16\u001b[0m     \u001b[0mori\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0msitk\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mWriteImage\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0morigin\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0mi\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m]\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mos\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mjoin\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mobjDir2\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0mfile\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m     17\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\n",
      "\u001b[0;32m~/anaconda3/envs/preprocess/lib/python3.9/site-packages/SimpleITK/extra.py\u001b[0m in \u001b[0;36m?\u001b[0;34m(image, fileName, useCompression, compressionLevel, imageIO, compressor)\u001b[0m\n",
      "\u001b[1;32m    421\u001b[0m     \u001b[0mwriter\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mSetUseCompression\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0museCompression\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m    422\u001b[0m     \u001b[0mwriter\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mSetCompressionLevel\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcompressionLevel\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m    423\u001b[0m     \u001b[0mwriter\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mSetImageIO\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mimageIO\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m    424\u001b[0m     \u001b[0mwriter\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mSetCompressor\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcompressor\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m--> 425\u001b[0;31m     \u001b[0;32mreturn\u001b[0m \u001b[0mwriter\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mExecute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mimage\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0m\n",
      "\u001b[0;32m~/anaconda3/envs/preprocess/lib/python3.9/site-packages/SimpleITK/SimpleITK.py\u001b[0m in \u001b[0;36m?\u001b[0;34m(self, *args)\u001b[0m\n",
      "\u001b[1;32m   7903\u001b[0m         \u001b[0mExecute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mImageFileWriter\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mImage\u001b[0m \u001b[0marg2\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mstd\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0mstring\u001b[0m \u001b[0mconst\u001b[0m \u001b[0;34m&\u001b[0m \u001b[0minFileName\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mbool\u001b[0m \u001b[0museCompression\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mint\u001b[0m \u001b[0mcompressionLevel\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m   7904\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m   7905\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[1;32m   7906\u001b[0m         \"\"\"\n",
      "\u001b[0;32m-> 7907\u001b[0;31m         \u001b[0;32mreturn\u001b[0m \u001b[0m_SimpleITK\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mImageFileWriter_Execute\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m*\u001b[0m\u001b[0margs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0m\n",
      "\u001b[0;31mTypeError\u001b[0m: Wrong number or type of arguments for overloaded function 'ImageFileWriter_Execute'.\n",
      "  Possible C/C++ prototypes are:\n",
      "    itk::simple::ImageFileWriter::Execute(itk::simple::Image const &)\n",
      "    itk::simple::ImageFileWriter::Execute(itk::simple::Image const &,std::string const &,bool,int)\n"
     ]
    }
   ],
   "source": [
    "for item in unique.items():\n",
    "    file=item[0]\n",
    "    slice=item[1][1]\n",
    "    if len(slice)>1 and len(slice)%2==1:\n",
    "        i=slice[int(len(slice)/2)]\n",
    "    elif len(slice)>1 and len(slice)%2==0:\n",
    "        i=slice[int(len(slice)/2)-1]\n",
    "    else:\n",
    "        i=slice[0]\n",
    "    seg=sitk.ReadImage(os.path.join(baseDir,file))\n",
    "    seg=sitk.GetArrayFromImage(seg)\n",
    "    origin=sitk.ReadImage(os.path.join(baseDir2,file))\n",
    "    origin=sitk.GetArrayFromImage(origin)\n",
    "    \n",
    "    s=sitk.WriteImage(seg[i,:,:],os.path.join(objDir,file))\n",
    "    ori=sitk.WriteImage(origin[i,:,:],os.path.join(objDir2,file))\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "for i in unique.items():\n",
    "    print(i[1][1][0])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "n=0\n",
    "for i in unique.items():\n",
    "    print(i)\n",
    "    if i[1][0]!=9:\n",
    "        n=n+1\n",
    "print(n)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "preprocess",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.19"
  },
  "orig_nbformat": 4
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
