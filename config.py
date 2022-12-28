# encoding:utf8
import torch

# 选择运行位置
device = torch.device(
    'cuda' if torch.cuda.is_available() else 'cpu'
)

# 预训练模型
Helsinki_en2zh = './Helsinki-NLP-opus-mt-en-zh'
Helsinki_zh2en = './Helsinki-NLP-opus-mt-zh-en'

liam_en2zh = './liam-168trans-opus-mt-en-zh'
liam_zh2en = './liam-168trans-opus-mt-zh-en'

nemo_en2zh = './nemo_en2zh/nmt_en_zh_transformer6x6.nemo'
nemo_zh2en = './nemo_zh2en/nmt_zh_en_transformer6x6.nemo'

# 语料
# 联合国文件平行语料
UN_en_dev = './UNv1.0.testsets/testsets/devset/UNv1.0.devset.en'
UN_zh_dev = './UNv1.0.testsets/testsets/devset/UNv1.0.devset.zh'
UN_en_test = './UNv1.0.testsets/testsets/testset/UNv1.0.testset.en'
UN_zh_test = './UNv1.0.testsets/testsets/testset/UNv1.0.testset.zh'
# 微博爬取语料
weibo_data = './corpus/data.cn-en.json'
# 正式文本语料（由联合国文件平行语料整理而得）
formal_zh_en = './corpus/formal_zh_en.jsonl'
# 非正式文本语料（由微博爬取语料筛选而得）
casual_zh_en = './corpus/casual_zh_en.jsonl'
# 特别测试用语料
attack1_txt = './corpus/attack1.txt'
attack1_jsonl = './corpus/attack1_zh_en.jsonl'
attack2_txt = './corpus/attack2.txt'
attack2_jsonl = './corpus/attack2_zh.jsonl'
attack3_txt = './corpus/attack3.txt'
attack3_jsonl = './corpus/attack3_en.jsonl'

# 翻译结果存放
result_dir = './translate_result'
# 由于发现按照16句一组，英译中出现了不少语料翻译重复的现象
# 例如Addendum（增编）翻译为增编增编增编……的情况
# 因此我们尝试令其以单句进行翻译
single_result_dir = './single_result'

# 分析文件存放目录
analysis_dir = './analysis'

# matplotlib制图用字体文件
font_file = './font/simsun.ttc'

# matplotlib图片存储位置
pictures_dir = './pictures'

# 统计结果存放文件
count_file = './count.txt'

# 问题语料存放位置
sentence_with_problem = './analysis'

# 评测数据及结果
zhen_result = './2000014125-秦宇航-zhen.txt'
enzh_result = './2000014125-秦宇航-enzh.txt'
