本仓库是本人自然语言处理导论第三次作业的源代码和结果<br>
仓库结构<br>
- preprocess.py 对语料的预处理<br>
- config.py 参数配置<br> 
- dataset.py 将语料拆分打包为数据集进行翻译<br>
- translate.py 执行翻译<br>
- get_similarity.py 计算参考答案和翻译结果的余弦相似度<br>
- get_leven_distance.py 计算参考答案和翻译结果的Levenshtein距离<br>
- get_sentence_with_problem.py 获取存在问题的语料<br>
- postprocess.py 对语料的后处理<br>
- corpus 所使用的语料<br>
- translate_result 翻译结果<br>
- analysis 计算平行语料的统计参数的结果<br>
- problems 根据统计参数得出的有问题的语料<br>