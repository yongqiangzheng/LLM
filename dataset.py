# ！/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/7 12:09
# @Author  : ZYQ
# @File    : dataset.py
# @Software: PyCharm
import re
import stanza
import xml.etree.ElementTree as ET

from tqdm import tqdm

# nlp = stanza.Pipeline('en', processors='tokenize', download_method=None)
sentiment_dict = {'negative': '-1', 'neutral': '0', 'positive': '1'}


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
            print(text)
            break
            aspect = aspectTerm.get('term')
            start = aspectTerm.get('from')
            end = aspectTerm.get('to')
            assert text[int(start):int(end)] == aspect
            data = {'sentence': text,
                    'aspect': aspect,
                    'polarity': sentiment_dict[polarity],
                    'aspect_index': [int(start), int(end)],
                    }
            dataset.append(data)
    return dataset


def write_dataset(file, dataset):
    fout = open(file, 'w')
    for dataset_item in tqdm(dataset):
        sentence = dataset_item['sentence']
        aspect = dataset_item['aspect']
        polarity = dataset_item['polarity']
        aspect_index = dataset_item['aspect_index']
        mask_sentence = sentence[:aspect_index[0]] + ' TARGET ' + sentence[aspect_index[1]:]
        tokens = [token.text for sentence in nlp(mask_sentence).sentences for token in sentence.tokens]
        tokenized_sentence = ' '.join(tokens)
        tokenized_sentence = tokenized_sentence.replace('TARGET', '$T$')
        tokenized_sentence = re.sub(' {2,}', ' ', tokenized_sentence)
        aspects = [token.text for aspect_word in nlp(aspect).sentences for token in aspect_word.tokens]
        tokenized_aspect = ' '.join(aspects)
        tokenized_aspect = re.sub(' {2,}', ' ', tokenized_aspect)

        fout.write(tokenized_sentence + '\n' + tokenized_aspect + '\n' + polarity + '\n')
    fout.close()

lap14_trainset = parse_xml(file='SemEval2014/Laptops_Train.xml')
# lap14_testset = parse_xml(file='SemEval2014/Laptops_Test.xml')
# rest14_trainset = parse_xml(file='SemEval2014/Restaurants_Train.xml')
# rest14_testset = parse_xml(file='SemEval2014/Restaurants_Test.xml')

# write_dataset('SemEval2014/Laptops_Train.txt', lap14_trainset)
# write_dataset('SemEval2014/Laptops_Test.txt', lap14_testset)
# write_dataset('SemEval2014/Restaurants_Train.txt', lap14_trainset)
# write_dataset('SemEval2014/Restaurants_Test.txt', lap14_testset)
