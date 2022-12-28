import jsonlines
import config


def get_data_from_one_file(
        model, source_lang, style
):
    """
    获取特定模型、特定翻译对、特定文本风格的翻译结果\n
    :param model: 模型名称(hel or liam)
    :param source_lang: 源语言(en or zh)
    :param style: 文本风格(formal, casual, attack1, attack2 or attack3)
    :return: 一个列表，元素为字典格式，字典包含源文本和结果
    """
    with jsonlines.open(
            './translate_result/{}-{}-{}.jsonl'.format(
                model, source_lang, style
            ),
            'r'
    ) as reader:
        return list(reader)


def get_enzh_data(style):
    """
    将特定风格的en翻译为zh的结果整理好传给主函数\n
    :param style: 文本风格(formal, casual, attack1 or attack3)
    :return: 一个列表，元素为写入评测结果文件的字符串
    """
    hel_data = get_data_from_one_file('hel', 'en', style)
    liam_data = get_data_from_one_file('liam', 'en', style)
    assert len(hel_data) == len(liam_data)
    res = [
        '{}\t{}\t{}\n'.format(
            hel_data[i]['source'], hel_data[i]['result'],
            liam_data[i]['result']
        )
        for i in range(len(hel_data))
    ]
    return res


def get_zhen_data(style):
    """
    将特定风格的zh翻译为en的结果整理好传给主函数\n
    :param style: 文本风格(formal, casual, or attack2)
    :return: 一个列表，元素为写入评测结果文件的字符串
    """
    hel_data = get_data_from_one_file('hel', 'zh', style)
    liam_data = get_data_from_one_file('liam', 'zh', style)
    assert len(hel_data) == len(liam_data)
    res = [
        '{}\t{}\t{}\n'.format(
            hel_data[i]['source'], hel_data[i]['result'],
            liam_data[i]['result']
        )
        for i in range(len(hel_data))
    ]
    return res


def main():
    zhen_list = get_zhen_data('formal') + \
        get_zhen_data('casual') + \
        get_zhen_data('attack2')
    with open(
        file=config.zhen_result,
        encoding='utf8',
        mode='w'
    ) as zhen_file:
        zhen_file.write('源文本\thel模型\tliam模型\n')
        zhen_file.writelines(zhen_list)

    enzh_list = get_enzh_data('formal') + \
        get_enzh_data('casual') + \
        get_enzh_data('attack1') + \
        get_enzh_data('attack3')
    with open(
        file=config.enzh_result,
        encoding='utf8',
        mode='w'
    ) as enzh_file:
        enzh_file.write('源文本\thel模型\tliam模型\n')
        enzh_file.writelines(enzh_list)


if __name__ == '__main__':
    main()
