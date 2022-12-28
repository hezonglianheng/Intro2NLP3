# encoding:utf8
import config
import jsonlines
from zhconv import convert
import re


def is_chinese(string: str):
    """
    用于筛选微博平行语料的函数之一（汉语部分是否为纯中文）\n
    :param string: 中文语料内容
    :return: 对语料是否为纯中文的判断，为bool值
    """
    for s in string:
        if re.search(
                pattern=r'[\u4e00-\u9fa5|，|。|！|、]',
                string=s
        ):
            continue
        else:
            return False
    return True


def is_english(string: str):
    """
    用于筛选微博平行语料的函数之一（英语部分是否为纯英文）\n
    :param string: 英文语料内容
    :return:对语料是否为纯英文的判断，为bool值
    """
    for s in string:
        if re.search(
                pattern=r'[A-Za-z0-9|.|,|\s]',
                string=s
        ):
            continue
        else:
            return False
    return True


def formal():
    """
    将联合国平行语料中的中文、英文语料保存到一个jsonlines文件中\n
    :return: 无返回值
    """
    with open(config.UN_zh_dev,
              mode='r', encoding='utf8') as f1:
        zh_corpus1 = f1.readlines()

    with open(config.UN_zh_test,
              mode='r', encoding='utf8') as f2:
        zh_corpus2 = f2.readlines()

    with open(config.UN_en_dev,
              mode='r', encoding='utf8') as f3:
        en_corpus1 = f3.readlines()

    with open(config.UN_en_test,
              mode='r', encoding='utf8') as f4:
        en_corpus2 = f4.readlines()

    assert len(zh_corpus1) == len(en_corpus1)
    assert len(zh_corpus2) == len(en_corpus2)

    parallel = []

    for i in range(len(zh_corpus1)):
        parallel.append(
            {
                'zh': zh_corpus1[i][:-1],
                'en': en_corpus1[i][:-1]
            }
        )

    for i in range(len(zh_corpus2)):
        parallel.append(
            {
                'zh': zh_corpus2[i][:-1],
                'en': en_corpus2[i][:-1]
            }
        )

    with jsonlines.open(config.formal_zh_en,
                        mode='w') as f:
        f.write_all(parallel)


def casual():
    """
    将微博平行语料保存在一个jsonlines格式文件中\n
    :return: 无返回值
    """
    with jsonlines.open(config.weibo_data,
                        mode='r') as weibo:
        parallel = [
            {
                'zh': convert(w['source'], 'zh-hans'),
                'en': w['target']
            }
            for w in weibo
            if is_chinese(w['source'])
               and is_english(w['target'])
        ]

    with jsonlines.open(config.casual_zh_en,
                        mode='w') as f:
        f.write_all(parallel)


def attack1():
    """
    将特别测试语料第一部分保存为jsonlines格式\n
    :return: 无
    """
    with open(config.attack1_txt,
              encoding='utf8', mode='r') as txt_f:
        sentences = txt_f.readlines()

    parallel = []
    for i in range(0, len(sentences), 2):
        parallel.append(
            {
                'en': sentences[i][:-1],
                'zh': sentences[i + 1][:-1]
            }
        )

    with jsonlines.open(
        config.attack1_jsonl,
        mode='w'
    ) as jsonl_f:
        jsonl_f.write_all(parallel)


def attack2():
    """
    将特别测试语料第二部分保存为jsonlines格式\n
    :return: 无
    """
    with open(config.attack2_txt,
              encoding='utf8', mode='r') as txt_f:
        sentences = txt_f.readlines()

    parallel = []
    for i in range(0, len(sentences)):
        parallel.append(
            {
                'en': '',
                'zh': sentences[i][:-1]
            }
        )

    with jsonlines.open(
            config.attack2_jsonl,
            mode='w'
    ) as jsonl_f:
        jsonl_f.write_all(parallel)


def attack3():
    """
    将特别测试语料第三部分保存为jsonlines格式\n
    :return: 无
    """
    with open(config.attack3_txt,
              encoding='utf8', mode='r') as txt_f:
        sentences = txt_f.readlines()

    parallel = []
    for i in range(0, len(sentences)):
        parallel.append(
            {
                'zh': '',
                'en': sentences[i][:-1]
            }
        )

    with jsonlines.open(
            config.attack3_jsonl,
            mode='w'
    ) as jsonl_f:
        jsonl_f.write_all(parallel)


if __name__ == '__main__':
    # formal()
    # casual()
    attack1()
    attack2()
    attack3()
