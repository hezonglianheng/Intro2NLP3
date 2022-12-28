# encoding:utf8
from transformers import MarianTokenizer, MarianMTModel
import config
from dataset import Dataset4Trans, Dataset4Nemo
import jsonlines
from tqdm import tqdm


# from nemo.collections.nlp.models import MTEncDecModel


def transform_translate(
        model_name, source_lang, style
):
    """使用Hugging Face提供的预训练模型进行翻译并保存结果为jsonlines格式
    :param model_name:预训练模型名称(hel or liam)
    :param source_lang:源语言(en or zh)
    :param style:文本风格(formal or casual or attack1 or attack2 or attack3)
    :return:无
    """
    if model_name == 'hel' and source_lang == 'en':
        path = config.Helsinki_en2zh
    elif model_name == 'hel' and source_lang == 'zh':
        path = config.Helsinki_zh2en
    elif model_name == 'liam' and source_lang == 'en':
        path = config.liam_en2zh
    elif model_name == 'liam' and source_lang == 'zh':
        path = config.liam_zh2en
    else:
        raise ValueError('Model name or language is wrong.')

    tokenizer = MarianTokenizer.from_pretrained(path)
    model = MarianMTModel.from_pretrained(path)
    model.to(config.device)

    data_set = Dataset4Trans(
        config.device, tokenizer, style, source_lang
    )
    batches = data_set.get_batches()  # 最终执行用
    # batches = data_set.get_single_sentence()  # 实验单句翻译用
    translate_result = []
    for b in tqdm(batches):
        generated_ids = model.generate(**b)
        translate_result.extend(tokenizer.batch_decode(
            generated_ids, skip_special_tokens=True
        ))

    trans_pairs = []
    assert len(data_set.texts) == len(translate_result)
    for i in range(len(data_set.texts)):
        trans_pairs.append(
            {
                'source': data_set.texts[i],
                'result': translate_result[i]
            }
        )

    with jsonlines.open(
            r'./translate_result/{}-{}-{}.jsonl'.format(
                model_name, source_lang, style
            ), mode='w'
    ) as file:
        file.write_all(trans_pairs)


def nemo_translate(source_lang, target_lang, style):
    if source_lang == 'en':
        nemo_path = config.nemo_en2zh
    elif source_lang == 'zh':
        nemo_path = config.nemo_zh2en
    else:
        raise ValueError('source language is wrong.')

    model = MTEncDecModel.restore_from(
        restore_path=nemo_path
    )
    dataset = Dataset4Nemo(source_lang, style)
    translations = model.translate(
        dataset.data,
        source_lang=source_lang,
        target_lang=target_lang
    )
    assert len(translations) == len(dataset.data)
    trans_pairs = []
    for i in range(len(dataset.data)):
        trans_pairs.append(
            {
                'source': dataset.data[i],
                'target': translations[i]
            }
        )

    with jsonlines.open(
            r'./translate_result/nemo-{}-{}.jsonl'.format(
                source_lang, style
            ), 'w'
    ) as writer:
        writer.write_all(trans_pairs)


if __name__ == '__main__':
    transform_translate('hel', 'zh', 'formal')
    transform_translate('hel', 'en', 'formal')
    transform_translate('hel', 'zh', 'casual')
    transform_translate('hel', 'en', 'casual')
    transform_translate('liam', 'zh', 'formal')
    transform_translate('liam', 'en', 'formal')
    transform_translate('liam', 'zh', 'casual')
    transform_translate('liam', 'en', 'casual')
    # nemo_translate('en', 'zh', 'formal')
    # nemo_translate('en', 'zh', 'casual')
    # nemo_translate('zh', 'en', 'formal')
    # nemo_translate('zh', 'en', 'casual')
    transform_translate('hel', 'en', 'attack1')
    transform_translate('hel', 'zh', 'attack2')
    transform_translate('hel', 'en', 'attack3')
    transform_translate('liam', 'en', 'attack1')
    transform_translate('liam', 'zh', 'attack2')
    transform_translate('liam', 'en', 'attack3')

