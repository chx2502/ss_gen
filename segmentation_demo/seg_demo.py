# !/usr/bin/python3
# -*-coding: utf8-*-

from segmentation import Dictionnary_Segmentation
from generate_segmentation import seg_file, wp_file, seg_file_wp, seg_memlist, wp_memlist, seg_memlist_wp


if __name__ == "__main__":

    sentences = ["汽车贷款怎么还款", "车贷如何申请", "车贷如何还款"]
    Custom_Dictionary_File = './dictionary/Custom_Dictionary.txt'  # 自定义词典
    Similar_Dictionary_File = './dictionary/Similar_Dictionary.txt'  # 相似问词典
    Keyword_Dictionary_File = './dictionary/Keyword_Dictionary.txt' # 关键词词典，做关键词筛选时才作为参数传入初始化函数

    # 创建 DS Dictionnary_Segmentation 用于分词和替换等功能，genertate_*.py 中的函数都以 DS 对象为参数传入
    DS = Dictionnary_Segmentation(Custom_Dictionary_File, Similar_Dictionary_File)
    DS.initialize_keyword_dictionary(Keyword_Dictionary_File)   # 关键词词典初始化

    seg_memlist_result = seg_memlist(sentences, DS)     # 对列表中的句子仅分词，结果以列表输出

    # 标准词替换后会把 "汽车贷款怎么还款" 换成 "车贷如何还款"
    # 会出现重复句子，函数内对结果做了去重处理
    wp_memlist_result = wp_memlist(sentences, DS)   # 对列表中的句子进行 标准词替换，不分词，结果以列表输出
    seg_memlist_wp_result = seg_memlist_wp(sentences, DS)   # 对列表中的句子进行 标准词替换，再进行分词，结果以列表输出

    print("仅分词：{}".format(seg_memlist_result))
    print("仅替换：{}".format(wp_memlist_result))
    print("替换+分词：{}".format(seg_memlist_wp_result))

    input_file = './input.txt'
    output_file_seg = './input_seg.txt'
    output_file_wp = './input_wp.txt'
    output_file_seg_wp = './input_seg_wp.txt'
    column = 2  # 要处理的句子在文件中的列号
    label = '1' # 文件中所有句子的标签（当时的需求是只做正例，就没有针对每一句的标签进行处理）

    seg_file(input_file, output_file_seg, column, label, DS)    # 从文件读入句子，分词，结果以文件输出
    wp_file(input_file, output_file_wp, column, label, DS)      # 从文件读入句子，用标准词替换，结果以文件输出
    seg_file_wp(input_file, output_file_seg_wp, column, label, DS)  # 从文件读入句子，用标准词替换，分词，结果以文件输出
