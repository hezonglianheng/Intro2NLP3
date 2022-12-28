import jsonlines
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import config


def draw_length_param_scatter(model, lang, style, p):
    """
    画出源文本长度-参数散点图\n
    :param model: 模型名称（hel or liam）
    :param lang: 目标语言（en or zh）
    :param style: 文本风格（formal, casual or attack1）
    :param p: 参数（cosine or levenshtein or edit1）
    :return:无
    """
    if lang == 'en':
        source = 'zh'
    elif lang == 'zh':
        source = 'en'
    else:
        raise AttributeError(
            'lang {} is wrong.'.format(lang)
        )

    if p == 'cosine':
        name = '余弦相似度'
        file_name = 'cosine'
    elif p == 'levenshtein':
        name = '编辑距离'
        file_name = 'levenshtein'
    elif p == 'edit1':
        name = '编辑距离/参考答案长度'
        file_name = 'levenshtein'
    else:
        raise AttributeError(
            'param {} is wrong.'.format(p)
        )

    with jsonlines.open(
            './analysis/{}-{}-{}-{}.jsonl'.format(
                model, lang, style, file_name
            ), 'r'
    ) as reader:
        sentences = list(reader)

    font = FontProperties(fname=config.font_file)
    fontdict = {"font": font, "size": 16}

    x = [len(s['source']) for s in sentences]
    if p == 'cosine':
        y = [s['similarity'] for s in sentences]
    elif p == 'levenshtein':
        y = [s['distance'] for s in sentences]
    elif p == 'edit1':
        y = [s['distance'] / len(s['standard'])
             for s in sentences]
    else:
        raise AttributeError(
            'the param {} is wrong.'.format(p)
        )

    plt.scatter(x, y, c='#4169E1', s=2)
    plt.title(
        label='{}模型{}文本类型从{}到{}翻译中\n源文本长度与{}的关系'.format(
            model, style, source, lang, name
        ),
        fontdict=fontdict
    )
    plt.xlabel(
        xlabel='文本长度', fontdict=fontdict
    )
    plt.ylabel(
        ylabel=name, fontdict=fontdict
    )
    plt.savefig(
        '{}/{}_{}_{}_{}.png'.format(
            config.pictures_dir, model, lang, style, p
        )
    )
    plt.show()


def draw_all_scatters(p):
    draw_length_param_scatter('hel', 'en', 'formal', p)
    draw_length_param_scatter('hel', 'en', 'casual', p)
    draw_length_param_scatter('hel', 'zh', 'formal', p)
    draw_length_param_scatter('hel', 'zh', 'casual', p)
    draw_length_param_scatter('liam', 'en', 'formal', p)
    draw_length_param_scatter('liam', 'en', 'casual', p)
    draw_length_param_scatter('liam', 'zh', 'formal', p)
    draw_length_param_scatter('liam', 'zh', 'casual', p)


def count(model, lang, style, p):
    """
    计算参量符合要求的文本数量及比例\n
    :param model: 模型名称（hel or liam）
    :param lang: 目标语言（en or zh）
    :param style: 文本风格（formal, casual or attack1）
    :param p: 参数（cosine or levenshtein or edit1）
    :return:无
    """
    if lang == 'en':
        source = 'zh'
    elif lang == 'zh':
        source = 'en'
    else:
        raise AttributeError(
            'lang {} is wrong.'.format(lang)
        )

    if p == 'cosine':
        file_name = 'cosine'
    elif p == 'levenshtein':
        file_name = 'levenshtein'
    elif p == 'edit1':
        file_name = 'levenshtein'
    else:
        raise AttributeError(
            'param {} is wrong.'.format(p)
        )

    with jsonlines.open(
            './analysis/{}-{}-{}-{}.jsonl'.format(
                model, lang, style, file_name
            ), 'r'
    ) as reader:
        sentences = list(reader)

    if p == 'cosine':
        ninty_five = len(
            [s for s in sentences if s['similarity'] > 0.95]
        )
        ninty_five_ratio = ninty_five / len(sentences)
        ninty = len(
            [s for s in sentences if s['similarity'] > 0.9]
        )
        ninty_ratio = ninty / len(sentences)
        eighty_five = len(
            [s for s in sentences if s['similarity'] > 0.85]
        )
        eighty_five_ratio = eighty_five / len(sentences)
        eighty = len(
            [s for s in sentences if s['similarity'] > 0.8]
        )
        eighty_ratio = eighty / len(sentences)

        return """
        {}模型{}文本类型从{}到{}翻译中{}参数
        总计语料{}条
        0.95以上有{}条，占比{}
        0.9以上有{}条，占比{}
        0.85以上有{}条，占比{}
        0.8以上有{}条，占比{}
        """.format(model, style, source, lang, p,
                   len(sentences),
                   ninty_five, ninty_five_ratio,
                   ninty, ninty_ratio,
                   eighty_five, eighty_five_ratio,
                   eighty, eighty_ratio)
    elif p == 'levenshtein':
        ten = len(
            [s for s in sentences if s['distance'] < 10]
        )
        ten_ratio = ten / len(sentences)
        twenty = len(
            [s for s in sentences if s['distance'] < 20]
        )
        twenty_ratio = twenty / len(sentences)
        forty = len(
            [s for s in sentences if s['distance'] < 40]
        )
        forty_ratio = forty / len(sentences)
        return """
        {}模型{}文本类型从{}到{}翻译中{}参数
        总计语料{}条
        距离10以下{}条，占比{}
        距离20以下{}条，占比{}
        距离40以下{}条，占比{}
        """.format(model, style, source, lang, p,
                   len(sentences),
                   ten, ten_ratio,
                   twenty, twenty_ratio,
                   forty, forty_ratio)
    elif p == 'edit1':
        point2 = len(
            [s for s in sentences
             if s['distance'] / len(s['standard']) < 0.2]
        )
        point2_ratio = point2 / len(sentences)
        point4 = len(
            [s for s in sentences
             if s['distance'] / len(s['standard']) < 0.4]
        )
        point4_ratio = point4 / len(sentences)
        point6 = len(
            [s for s in sentences
             if s['distance']/ len(s['standard']) < 0.6]
        )
        point6_ratio = point6 / len(sentences)
        return """
        {}模型{}文本类型从{}到{}翻译中{}参数
        总计语料{}条
        0.2以下{}条，占比{}
        0.4以下{}条，占比{}
        0.6以下{}条，占比{}
        """.format(model, style, source, lang, p,
                   len(sentences),
                   point2, point2_ratio,
                   point4, point4_ratio,
                   point6, point6_ratio)


def count_all():
    with open('./count.txt',
              encoding='utf8', mode='w') as file:
        file.write(count('hel', 'en', 'formal', 'cosine'))
        file.write(count('hel', 'en', 'casual', 'cosine'))
        file.write(count('hel', 'zh', 'formal', 'cosine'))
        file.write(count('hel', 'zh', 'casual', 'cosine'))
        file.write(count('liam', 'en', 'formal', 'cosine'))
        file.write(count('liam', 'en', 'casual', 'cosine'))
        file.write(count('liam', 'zh', 'formal', 'cosine'))
        file.write(count('liam', 'zh', 'casual', 'cosine'))
        file.write(count('hel', 'en', 'formal', 'levenshtein'))
        file.write(count('hel', 'en', 'casual', 'levenshtein'))
        file.write(count('hel', 'zh', 'formal', 'levenshtein'))
        file.write(count('hel', 'zh', 'casual', 'levenshtein'))
        file.write(count('liam', 'en', 'formal', 'levenshtein'))
        file.write(count('liam', 'en', 'casual', 'levenshtein'))
        file.write(count('liam', 'zh', 'formal', 'levenshtein'))
        file.write(count('liam', 'zh', 'casual', 'levenshtein'))
        file.write(count('hel', 'en', 'formal', 'edit1'))
        file.write(count('hel', 'en', 'casual', 'edit1'))
        file.write(count('hel', 'zh', 'formal', 'edit1'))
        file.write(count('hel', 'zh', 'casual', 'edit1'))
        file.write(count('liam', 'en', 'formal', 'edit1'))
        file.write(count('liam', 'en', 'casual', 'edit1'))
        file.write(count('liam', 'zh', 'formal', 'edit1'))
        file.write(count('liam', 'zh', 'casual', 'edit1'))


if __name__ == '__main__':
    count_all()
