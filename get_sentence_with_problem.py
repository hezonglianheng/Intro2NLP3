import jsonlines


def get_sentences(model, lang, style, parameter):
    """
    获取不同模型、不同语言、不同文本风格、不同计算参数下表现最差的前10%句子以发现不同条件下模型表现的问题\n
    :param model: 模型名称(hel or liam)
    :param lang: 翻译目标语言(en or zh)
    :param style: 翻译文本风格(formal or casual)
    :param parameter: 使用的参数值(cosine or levenshtein)
    :return: 无
    """
    with jsonlines.open(
        './analysis/{}-{}-{}-{}.jsonl'.format(
            model, lang, style, parameter
        ), mode='r'
    ) as reader:
        sentences = list(reader)

    if parameter == 'cosine':
        sentences.sort(key=lambda x: x['similarity'])
    elif parameter == 'levenshtein':
        # 获取编辑距离/源文本长度最大的句子
        sentences.sort(
            key=lambda x: x['distance']/len(x['source']),
            reverse=True
        )

    with jsonlines.open(
        './problems/{}-{}-{}-{}.jsonl'.format(
            model, lang, style, parameter
        ), mode='w'
    ) as writer:
        writer.write_all(sentences[:len(sentences)//10])


def get_all():
    """
    遍历所有的情况，获取该情况下表现最差的前10%语料，分别写入jsonl文件中\n
    :return: 无
    """
    get_sentences('hel', 'en', 'formal', 'cosine')
    get_sentences('hel', 'en', 'casual', 'cosine')
    get_sentences('hel', 'zh', 'formal', 'cosine')
    get_sentences('hel', 'zh', 'formal', 'cosine')
    get_sentences('hel', 'zh', 'casual', 'cosine')
    get_sentences('liam', 'en', 'formal', 'cosine')
    get_sentences('liam', 'en', 'casual', 'cosine')
    get_sentences('liam', 'zh', 'formal', 'cosine')
    get_sentences('liam', 'zh', 'casual', 'cosine')
    get_sentences('hel', 'en', 'formal', 'levenshtein')
    get_sentences('hel', 'en', 'casual', 'levenshtein')
    get_sentences('hel', 'zh', 'formal', 'levenshtein')
    get_sentences('hel', 'zh', 'casual', 'levenshtein')
    get_sentences('liam', 'en', 'formal', 'levenshtein')
    get_sentences('liam', 'en', 'casual', 'levenshtein')
    get_sentences('liam', 'zh', 'formal', 'levenshtein')
    get_sentences('liam', 'zh', 'casual', 'levenshtein')


if __name__ == '__main__':
    get_all()
