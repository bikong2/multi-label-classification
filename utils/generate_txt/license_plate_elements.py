# -*- coding: utf-8 -*-
"""
File license_plate_elements.py
@author:ZhengYuwei
功能：
定义车牌相关的元素，包括车牌中的字符和车牌类型
一般车牌字符一共7位，新能源车牌8位，故增加一个标志位，表示车牌位数
plate_type_enum为车牌类型，is_exist_plate_enum标记是否存在车牌
"""


class LicensePlateElements(object):
    """ 定义车牌相关的元素（车牌字符和车牌类型），以及获取元素的方法
    一般车牌字符一共7位，新能源车牌8位，故增加一个标志位，表示车牌位数
    plate_type_enum为车牌类型，is_exist_plate_enum标记是否存在车牌
    """

    # 车牌第1位字符的取值范围及其label
    char1_enum = {
        u"京": 0, u"沪": 1, u"津": 2, u"渝": 3, u"冀": 4, u"晋": 5, u"蒙": 6, u"辽": 7, u"吉": 8, u"黑": 9,
        u"苏": 10, u"浙": 11, u"皖": 12, u"闽": 13, u"赣": 14, u"鲁": 15, u"豫": 16, u"鄂": 17, u"湘": 18, u"粤": 19,
        u"桂": 20, u"琼": 21, u"川": 22, u"贵": 23, u"云": 24, u"藏": 25, u"陕": 26, u"甘": 27, u"青": 28, u"宁": 29,
        u"新": 30, u"军": 31, u"使": 32, u"WJ": 33,
    }

    # 车牌第2位字符的取值范围及其label
    char2_enum = {
        "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "J": 8, "K": 9,
        "L": 10, "M": 11, "N": 12, "P": 13, "Q": 14, "R": 15, "S": 16, "T": 17, "U": 18, "V": 19,
        "W": 20, "X": 21, "Y": 22, "Z": 23, "0": 24, "1": 25, "2": 26, "3": 27, "4": 28, "5": 29,
        "6": 30, "7": 31, "8": 32, "9": 33, u"京": 34, u"沪": 35, u"津": 36, u"渝": 37, u"冀": 38, u"晋": 39,
        u"蒙": 40, u"辽": 41, u"吉": 42, u"黑": 43, u"苏": 44, u"浙": 45, u"皖": 46, u"闽": 47, u"赣": 48, u"鲁": 49,
        u"豫": 50, u"鄂": 51, u"湘": 52, u"粤": 53, u"桂": 54, u"琼": 55, u"川": 56, u"贵": 57, u"云": 58, u"藏": 59,
        u"陕": 60, u"甘": 61, u"青": 62, u"宁": 63, u"新": 64,
    }

    # 车牌第3~6位字符的取值范围及其label
    char3_6_enum = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "J": 18, "K": 19,
        "L": 20, "M": 21, "N": 22, "P": 23, "Q": 24, "R": 25, "S": 26, "T": 27, "U": 28, "V": 29,
        "W": 30, "X": 31, "Y": 32, "Z": 33,
    }

    # 车牌第7位字符的取值范围及其label
    char7_enum = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16, "H": 17, "J": 18, "K": 19,
        "L": 20, "M": 21, "N": 22, "P": 23, "Q": 24, "R": 25, "S": 26, "T": 27, "U": 28, "V": 29,
        "W": 30, "X": 31, "Y": 32, "Z": 33, u"学": 34, u"警": 35, u"领": 36, u"挂": 37, u"港": 38, u"澳": 39,
        u"使": 40, u"应急": 41,
    }

    # 车牌第8位字符的取值范围及其label
    char8_enum = {
        "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "D": 10, "F": 11,
    }

    # 车牌位数及其label
    char_number_enum = {'7': 0, '8': 1}

    # 车牌类型
    plate_colors = {
        'blue': 0, 'yellow': 1, 'green': 2, 'white': 3, 'black': 4, 'other': 5,
    }

    # 车牌类型
    plate_type_enum = {
        'single_blue': 0, 'single_yellow': 1, 'double_yellow': 2, 'police': 3, 'learner': 4,
        'hk': 5, 'macau': 6, 'single_army': 7, 'double_army': 8, 'consulate': 9,
        'embassy': 10, 'army_police': 11, 'double_army_police': 12, 'small_new_energy': 13, 'big_new_energy': 14,
        'factory': 15, 'single_black': 16, 'other': 17,
    }

    # 是否存在车牌
    is_exist_plate_enum = {'exist': 0, 'non-exist': 1}

    # 不同车牌位置与车牌字符变量取值表的映射表
    index_to_char_label = {
        0: char1_enum,
        1: char2_enum,
        2: char3_6_enum,
        3: char3_6_enum,
        4: char3_6_enum,
        5: char3_6_enum,
        6: char7_enum,
        7: char8_enum,
        8: char_number_enum,
        9: plate_colors,
        10: is_exist_plate_enum,
    }

    def __init__(self):
        """ 初始化，通过每一位车牌字符的char_label，增加label_char的反向映射 """
        self.index_to_label_char = {}
        for index, char_label in LicensePlateElements.index_to_char_label.items():
            self.index_to_label_char[index] = {label: char for char, label in char_label.items()}

        self.label_to_type = {}
        for label, plate_type in LicensePlateElements.plate_type_enum.items():
            self.label_to_type[label] = plate_type
        return

    def get_char_label(self, index):
        """ 获取指定车牌位置的char-label映射
        :param index: 指定车牌位数
        :return: 指定车牌位置的char-label映射
        """
        return self.index_to_char_label.get(index, None)

    def get_label_char(self, index):
        """ 获取指定车牌位置的label-char映射
        :param index: 指定车牌位数
        :return: 指定车牌位置的label-char映射
        """
        return self.index_to_label_char.get(index, None)

    def get_chars_sorted_by_label(self, index):
        """ 获取指定车牌位置上，按label排序的字符列表
        :param index: 指定车牌位置
        :return: 字符列表
        """
        label_char = self.get_label_char(index)
        if label_char is None:
            raise ValueError('Index is Out of Maximal License Plate Figures')
        chars = [None] * len(label_char)
        for index, char in label_char.items():
            chars[index] = char
        return chars

    def get_char(self, index, label):
        """ 获取指定车牌位数、标签的对应字符
        :param index: 指定车牌位数
        :param label: 指定标签
        :return: 车牌字符
        """
        label_char = self.index_to_label_char.get(index, None)
        if label_char is None:
            print('Index is Out of Maximal License Plate Figures')
            return None
        return label_char.get(label, None)

    def get_label(self, index, char):
        """ 获取指定车牌位数、字符的对应标签
        :param index: 指定车牌位置
        :param char: 指定字符
        :return: 车牌标签
        """
        char_label = self.index_to_char_label.get(index, None)
        if char_label is None:
            print('Index is Out of Maximal License Plate Figures')
            return None
        return char_label.get(char, None)

    def convert_to_labels(self, license_plate):
        """ 将车牌号转换为标签
        :param license_plate: 车牌号
        :return: 标签
        """
        plate_len = len(license_plate)
        i = 0
        if plate_len != 7 and plate_len != 8:
            return None

        if license_plate[0:2] == 'WJ':
            labels: list = [None] * (plate_len - 1)
            labels[0] = self.get_label(0, license_plate[0:2])
            license_plate = license_plate[1:]
            plate_len -= 1
            i = 1
        elif license_plate[6:8] == '应急':
            labels: list = [None] * (plate_len - 1)
            labels[6] = self.get_label(6, license_plate[6:8])
            plate_len -= 2
        else:
            labels: list = [None] * plate_len

        while i < plate_len:
            labels[i] = self.get_label(i, license_plate[i])
            i += 1
        return labels

    def get_type_list(self):
        """ 获取车牌类型有序（label序）列表 """
        type_list = [None] * len(self.plate_type_enum)
        for plate_type, label in self.plate_type_enum.items():
            type_list[label] = plate_type
        return type_list

    def get_type(self, label):
        """ 根据车配类型的label，获取车牌类型
        :param label: 车牌类型的label
        :return:
        """
        return self.label_to_type[label]
