# -*- coding: utf-8 -*-
"""
File file_tools.py
@author:ZhengYuwei
"""
import os
import random
import datetime
import cv2
from utils.generate_txt.file_tools import FileTools
from utils.generate_txt.license_plate_elements import LicensePlateElements

# 所有车牌号图片的根目录
plate_images_root_dir = '/home/data_159/data1/license_plate/plate_recognition/new_plate_images/'

blue_dir = [plate_images_root_dir + 'download/blue',
            plate_images_root_dir + 'project_cloud/truth_blue',
            plate_images_root_dir + 'project_cloud/deepercut_blue']

yellow_dir = [plate_images_root_dir + 'download/yellow',
              plate_images_root_dir + 'project_cloud/truth_yellow',
              plate_images_root_dir + 'project_cloud/deepercut_yellow']

green_dir = [plate_images_root_dir + 'download/green',
             plate_images_root_dir + 'project_cloud/truth_green',
             plate_images_root_dir + 'project_cloud/deepercut_green']

white_dir = [plate_images_root_dir + 'download/white',
             plate_images_root_dir + 'project_cloud/truth_white',
             plate_images_root_dir + 'project_cloud/deepercut_white']

black_dir = [plate_images_root_dir + 'download/black', ]

unknown_dir = [plate_images_root_dir + 'project_cloud/truth_unknown',
               plate_images_root_dir + 'project_cloud/deepercut_unknown']
unknown_dir = list()  # 由于unknown数据集的数据质量太差了，不加入进行训练


# 所有车牌图片路径list
def search_images(root_paths):
    image_paths = list()
    for path in root_paths:
        print('搜索路径', path)
        image_paths.extend(FileTools.search_file(path, '.jpg'))
    return image_paths


blue_paths = search_images(blue_dir)
yellow_paths = search_images(yellow_dir)
green_paths = search_images(green_dir)
white_paths = search_images(white_dir)
black_paths = search_images(black_dir)
unknown_paths = search_images(unknown_dir)

# 生成标签数据（其中图片路径是相对根目录的路径）
print('开始产生车牌号标签列表...')
plate_nums = (len(blue_paths), len(yellow_paths), len(green_paths),
              len(white_paths), len(black_paths), len(unknown_paths))
print('blue, yellow, green, white, black, unknown:{}'.format(plate_nums))
elements = LicensePlateElements()
all_paths = (blue_paths, yellow_paths, green_paths, white_paths, black_paths, unknown_paths)
types = (str(elements.plate_colors['blue']), str(elements.plate_colors['yellow']),
         str(elements.plate_colors['green']), str(elements.plate_colors['white']),
         str(elements.plate_colors['black']), '-1')
lines = list()
char8_labels = '-1'
plate7_type = str(elements.char_number_enum.get('7'))
plate8_type = str(elements.char_number_enum.get('8'))
line: list = [None] * 11
check_list = list()
for path_index, paths in enumerate(all_paths):
    for image_index, image_path in enumerate(paths):
        img = cv2.imread(image_path)
        if img is None:
            check_list.append(image_path)
            continue
        plate_no = os.path.splitext(os.path.basename(image_path))[0].split('_')[-1]  # 00000001_xxxxxxxx.jpg
        labels = elements.convert_to_labels(plate_no)
        if labels is None:
            check_list.append(image_path)
            continue
        # relative_path char1 char2 char3 char4 char5 char6 char7 char8 char_num plate_color
        line[0] = image_path[len(plate_images_root_dir):]
        if len(labels) == 7:
            line[1:8] = [str(label) for label in labels]
            line[8] = char8_labels
            line[9] = plate7_type
        elif len(labels) == 8:
            line[1:9] = [str(label) for label in labels]
            line[9] = plate8_type
        else:
            check_list.append(image_path)
            continue
        line[10] = types[path_index]
        lines.append([' '.join(line), '\n'])
        if (image_index + 1) % 10000 == 0:
            print('{}: {}/{} done...'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                             image_index + 1, plate_nums[path_index]))

print('生成数据标签文件（{}）...'.format(len(lines)))
random.shuffle(lines)
all_txt, test_txt, validate_txt, train_txt = 'all.txt', 'test.txt', 'val.txt', 'train.txt'
with open(all_txt, 'w+') as all_file, open(test_txt, 'w+') as test_file, \
        open(validate_txt, 'w+') as validate_file, open(train_txt, 'w+') as train_file:
    for line in lines:
        all_file.writelines(line)
        if line[0].find('test') != -1:
            test_file.writelines(line)
        elif line[0].find('val') != -1:
            validate_file.writelines(line)
        else:
            train_file.writelines(line)
