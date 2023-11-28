# ！/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/7 12:09
# @Author  : ZYQ
# @File    : dataset.py
# @Software: PyCharm
import xml.etree.ElementTree as ET

from tqdm import tqdm


def parse_xml(file):
    dataset = []
    tree = ET.parse(file)  # 解析树
    root = tree.getroot()  # 根节点
    for sentence in tqdm(root.findall('sentence')):
        aspectTerms = sentence.find('aspectTerms')
        if aspectTerms is None:  # 去掉没有aspect的句子
            continue
        text = sentence.find('text').text  # 句子
        for aspectTerm in aspectTerms.findall('aspectTerm'):  # 遍历所有的aspect
            polarity = aspectTerm.get('polarity').strip()
            if polarity == 'conflict':  # 去掉conflict情感的句子
                continue
            aspect = aspectTerm.get('term')
            data = {'sentence': text,
                    'aspect': aspect,
                    'polarity': polarity,
                    }
            dataset.append(data)
    return dataset


def write_dataset(file, dataset):
    fout = open(file, 'w')
    for dataset_item in tqdm(dataset):
        sentence = dataset_item['sentence']
        aspect = dataset_item['aspect']
        polarity = dataset_item['polarity']
        fout.write(sentence + '\n' + aspect + '\n' + polarity + '\n')
    fout.close()

lap14_trainset = parse_xml(file='SemEval2014/Laptops_Train.xml')
lap14_testset = parse_xml(file='SemEval2014/Laptops_Test.xml')
rest14_trainset = parse_xml(file='SemEval2014/Restaurants_Train.xml')
rest14_testset = parse_xml(file='SemEval2014/Restaurants_Test.xml')

write_dataset('SemEval2014/Laptops_Train.txt', lap14_trainset)
write_dataset('SemEval2014/Laptops_Test.txt', lap14_testset)
write_dataset('SemEval2014/Restaurants_Train.txt', lap14_trainset)
write_dataset('SemEval2014/Restaurants_Test.txt', lap14_testset)
