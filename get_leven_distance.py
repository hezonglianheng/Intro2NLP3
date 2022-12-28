# encoding: utf8
import jsonlines
import spacy
import numpy as np


def get_leven_distance(list1, list2):
    """
    给定已被词切分为列表的字符串，计算其编辑距离并返回\n
    :param list1: 一个字符串被按词拆分后的列表
    :param list2: 一个字符串被按词拆分后的列表
    :return: 整数，表示两个字符串的编辑距离
    """
    # 初始化一个矩阵储存计算结果，大小为(len(list1)+1, len(list2)+1)
    leven_matrix = np.zeros((len(list1)+1, len(list2)+1))
    # 初始化第一行和第一列的值
    for i in range(len(list1)+1):
        leven_matrix[i][0] = i
    for j in range(len(list2)+1):
        leven_matrix[0][j] = j
    # 计算其他位置的编辑距离。(i, j)位置编辑距离的计算为：
    # (i-1, j)位置的值+1
    # (i, j-1)位置的值+1
    # (i-1, j-1)位置的值+(若i位置字符和j位置字符不同为1，否则0)
    # 取其中最小值。
    for i in range(1, len(list1)+1):
        for j in range(1, len(list2)+1):
            if list1[i-1] == list2[j-1]:
                flag = 0
            else:
                flag = 1
            leven_matrix[i][j] = min(
                leven_matrix[i-1][j]+1,
                leven_matrix[i][j-1]+1,
                leven_matrix[i-1][j-1]+flag
            )

    return int(leven_matrix[len(list1)][len(list2)])


def run(model: str, lang: str, style: str):
    """
    用spacy库进行tokenization\n
    之后计算参考答案和工具包翻译结果之间的编辑距离并保存\n
    :param model: 模型名称(liam or hel)
    :param lang: 翻译结果语言(en or zh)
    :param style: 文本风格(formal, casual or attack1)
    :return:无
    """
    # 获得源语言信息
    if lang == 'en':
        source = 'zh'
    elif lang == 'zh':
        source = 'en'
    else:
        raise ValueError('language {} is wrong.'.format(lang))
    # 获取模型名称并加载模型
    name = '{}_core_web_sm'.format(lang)
    nlp = spacy.load(name)
    # 获取标准答案对
    with jsonlines.open(
        './corpus/{}_zh_en.jsonl'.format(style), 'r'
    ) as r1:
        standard = list(r1)
    # 获得翻译结果
    with jsonlines.open(
        './translate_result/{}-{}-{}.jsonl'.format(
            model, source, style
        ), 'r'
    ) as r2:
        answer = list(r2)
    # 获得全部编辑距离
    assert len(standard) == len(answer)
    compare = []
    for i in range(len(standard)):
        doc1 = nlp(standard[i][lang])
        doc2 = nlp(answer[i]['result'])
        lst1 = [token.text for token in doc1]
        lst2 = [token.text for token in doc2]
        distance = get_leven_distance(lst1, lst2)
        compare.append(
            {
                'source': answer[i]['source'],
                'standard': standard[i][lang],
                'answer': answer[i]['result'],
                'distance': distance
            }
        )
    # 保存
    with jsonlines.open(
        './analysis/{}-{}-{}-levenshtein.jsonl'.format(
            model, lang, style
        ), 'w'
    ) as w:
        w.write_all(compare)


if __name__ == '__main__':
    run('hel', 'en', 'casual')
    run('hel', 'en', 'formal')
    run('hel', 'zh', 'casual')
    run('hel', 'zh', 'formal')
    run('liam', 'en', 'casual')
    run('liam', 'en', 'formal')
    run('liam', 'zh', 'casual')
    run('liam', 'zh', 'formal')
    run('hel', 'zh', 'attack1')
    run('liam', 'zh', 'attack1')
