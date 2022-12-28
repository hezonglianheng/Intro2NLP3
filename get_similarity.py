import spacy
import jsonlines


def get_similarity(model_name, lang, style):
    """
    用spacy库计算文本余弦距离以考察参考译文和ML系统答案的接近程度，并保存在analysis目录下\n
    :param model_name: 模块名（hel或liam）
    :param lang: 翻译结果语言（en或zh）
    :param style: 文本风格（formal或casual或attack1）
    :return:无
    """
    if lang == 'en':
        source = 'zh'
    elif lang == 'zh':
        source = 'en'
    else:
        raise ValueError(
            'target language {} is wrong.'.format(lang)
        )

    if lang == 'en' or lang == 'zh':
        # 确定应用的模型
        # name = '{}_core_web_sm'.format(lang)  # 用于在本地进行sanity check
        name = '{}_core_web_lg'.format(lang)  # 实际在远程服务器上执行
    else:
        raise ValueError(
            'the language {} is wrong.'.format(lang)
        )

    nlp = spacy.load(name)

    with jsonlines.open(
        './corpus/{}_zh_en.jsonl'.format(style), 'r'
    ) as r1:
        standard = list(r1)

    with jsonlines.open(
        './translate_result/{}-{}-{}.jsonl'.format(
            model_name, source, style
        ), 'r'
    ) as r2:
        answer = list(r2)

    assert len(standard) == len(answer)

    compare = []
    for i in range(len(standard)):
        doc1 = nlp(standard[i][lang])
        doc2 = nlp(answer[i]['result'])
        similarity = doc1.similarity(doc2)
        compare.append(
            {
                'source': answer[i]['source'],
                'standard': standard[i][lang],
                'answer': answer[i]['result'],
                'similarity': similarity
            }
        )

    # compare.sort(key=lambda x: x['similarity'])  # 按相似度排序
    with jsonlines.open(
        './analysis/{}-{}-{}-cosine.jsonl'.format(
            model_name, lang, style
        ), 'w'
    ) as w:
        w.write_all(compare)


if __name__ == '__main__':
    get_similarity('hel', 'en', 'casual')
    get_similarity('hel', 'en', 'formal')
    get_similarity('hel', 'zh', 'casual')
    get_similarity('hel', 'zh', 'formal')
    get_similarity('liam', 'en', 'casual')
    get_similarity('liam', 'en', 'formal')
    get_similarity('liam', 'zh', 'casual')
    get_similarity('liam', 'zh', 'formal')
    get_similarity('hel', 'zh', 'attack1')
    get_similarity('liam', 'zh', 'attack1')