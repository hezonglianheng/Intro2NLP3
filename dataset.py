# encoding: utf8
import config
import jsonlines


class Dataset4Trans:
    """
    为Hugging Face模型建立的dataset\n
    device:所用的计算设备，cuda or cpu\n
    tokenizer:分词器\n
    style:文本风格，决定使用的原始语料\n
    lang:dataset的语言\n
    """

    def __init__(self, device, tokenizer, style, lang):
        self.device = device  # cuda or cpu
        self.tokenizer = tokenizer  # 由模型决定
        self.style = style  # formal or casual or
        self.lang = lang  # en or zh
        self.file = self._get_file()
        self.texts = self._get_texts()

    def _get_file(self):
        """
        根据self.style决定获取语料的文件\n
        :return:
        """
        if self.style == 'formal':
            return config.formal_zh_en
        elif self.style == 'casual':
            return config.casual_zh_en
        elif self.style == 'attack1':
            return config.attack1_jsonl
        elif self.style == 'attack2':
            return config.attack2_jsonl
        elif self.style == 'attack3':
            return config.attack3_jsonl
        else:
            raise ValueError(
                'style {} is wrong!'.format(self.style)
            )

    def _get_texts(self):
        """
        获取语料\n
        :return:
        """
        with jsonlines.open(self.file, 'r') as reader:
            if self.lang == 'en':
                return [r['en'] for r in reader]
            elif self.lang == 'zh':
                return [r['zh'] for r in reader]
            else:
                raise ValueError(
                    'language {} is wrong!'.format(self.lang)
                )

    def get_batches(self):
        """
        将语料分为16句一组，分组获得结果，以免炸掉显存\n
        :return: 几组分别padding的向量和其attention_mask
        """
        groups = []
        inputs = []
        for i in range(0, len(self.texts), 16):
            groups.append(self.texts[i: i+16])
        rest = len(self.texts) % 16
        # 剩余语料单独一组
        # groups.append(self.texts[len(self.texts)-rest:])
        for g in groups:
            batch = self.tokenizer(
                g, padding=True, return_tensors='pt'
            )
            for b in batch:
                batch[b] = batch[b].to(self.device)
            inputs.append(batch)
        return inputs

    def get_single_sentence(self):
        """
        将语料分为一句一组获得结果，实验一句一组的效果\n
        实验没有效果，弃用这一函数\n
        :return: 所有语料的向量
        """
        sentences = []
        inputs = []
        for i in range(len(self.texts)):
            sentences.append([self.texts[i]])
        for s in sentences:
            batch = self.tokenizer(
                s, return_tensors='pt'
            )
            for b in batch:
                batch[b] = batch[b].to(self.device)
            inputs.append(batch)
        return inputs


class Dataset4Nemo:
    """
    为Nemo分词设计的dataset\n
    lang:dataset语言\n
    style:文本风格，决定使用的原始语料\n
    """
    def __init__(self, lang, style):
        self.lang = lang
        self.style = style
        self.file = self._get_file()
        self.data = self._get_data()

    def _get_file(self):
        if self.style == 'formal':
            return config.formal_zh_en
        elif self.style == 'casual':
            return config.casual_zh_en
        else:
            raise ValueError(
                'style {} is wrong!'.format(self.style)
            )

    def _get_data(self):
        with jsonlines.open(self.file, 'r') as reader:
            if self.lang == 'en':
                return [r['en'] for r in reader]
            elif self.lang == 'zh':
                return [r['zh'] for r in reader]
            else:
                raise ValueError('language {} is wrong!')


if __name__ == '__main__':
    from transformers import MarianTokenizer

    tokenizer = MarianTokenizer.from_pretrained(
        config.Helsinki_zh2en
    )
    dataset = Dataset4Trans(
        config.device, tokenizer, 'casual', 'zh'
    )
    print(dataset.get_single_sentence()[0])
    print(dataset.get_batches()[0])
