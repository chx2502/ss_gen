# !/usr/bin/python3
# -*-coding: utf8-*-

from segmentation import Dictionnary_Segmentation


def seg_memlist(sentences_list, DS: Dictionnary_Segmentation):
    """
    输入一个句子列表，输出按自定义词典分词后的句子列表，用空格分割
    :param sentences_list: 原句列表
    :param DS: Dictionnary_Segmentation 对象，用于分词
    :return: list
    """
    result = []
    for sentence in sentences_list:
        result.append(' '.join(DS.segmentation_without_replace(sentence)))
    return result


def wp_memlist(sentences_list, DS: Dictionnary_Segmentation):
    """
    输入一个句子列表，将其中的词替换成同义词表里的标准词，输出替换后的句子列表
    :param sentences_list: 原句列表
    :param DS: Dictionnary_Segmentation 对象，用于替换
    :return: list
    """
    result = []
    for sentence in sentences_list:
        result.append(''.join(DS.CustomDictionary_Segmentation(sentence)))
    # 进行标准词替换后可能出现重复句
    result = list(set(result))
    return result


def seg_memlist_wp(sentences_list, DS: Dictionnary_Segmentation):
    """
    输入一个句子列表，将其中的词替换成同义词表里的标准词,
    输出按自定义词典分词后的句子列表，用空格分割
    :param sentences_list: 原句列表
    :param DS: Dictionnary_Segmentation 对象，用于替换和分词
    :return: list
    """
    result = []
    for sentence in sentences_list:
        result.append(' '.join(DS.CustomDictionary_Segmentation(sentence)))
    # 进行标准词替换后可能出现重复句
    result = list(set(result))
    return result


def seg_file(input_file, output_file, column, label, DS: Dictionnary_Segmentation):
    """
    输入句子文件，输出分词后的文件
    :param input_file: 输入文件
    :param output_file: 输出文件
    :param column: 需要分词的句子所在的列号
    :param label: 所有分词句子的标签（目前的需求全是正例，故标签统一，需求变化时要考虑修改）
    :param DS: Dictionnary_Segmentation 对象，用于分词
    :return: null
    """
    # 输入句子去重
    txtlines = list(set(open(input_file, "r+", encoding='utf-8').readlines()))
    output_file = open(output_file, 'w+', encoding='utf-8')

    original_sentences = []
    for txtline in txtlines:
        original_sentences.append(txtline.replace('\n', '').split('\t')[column-1])
    segmented_sentences = seg_memlist(original_sentences, DS)
    for origin, seg in zip(original_sentences, segmented_sentences):
            write_line = "{}\t{}\t{}\n".format(origin, seg, label)
            # print("写入：" + write_line)
            output_file.write(write_line)

    output_file.close()


def wp_file(input_file, output_file, column, label, DS: Dictionnary_Segmentation):
    """
    输入句子文件，输出用标准词替换后的文件
    :param input_file: 输入文件
    :param output_file: 输出文件
    :param column: 需要替换的句子所在的列号
    :param label: 所有句子的标签（目前的需求全是正例，故标签统一，需求变化时要考虑修改）
    :param DS: Dictionnary_Segmentation 对象，用于替换
    :return: null
    """
    # 输入句子去重
    txtlines = list(set(open(input_file, "r+", encoding='utf-8').readlines()))
    output_file = open(output_file, 'w+', encoding='utf-8')

    original_sentences = []
    for txtline in txtlines:
        original_sentences.append(txtline.replace('\n', '').split('\t')[column-1])
    segmented_sentences = wp_memlist(original_sentences, DS)
    for origin, seg in zip(original_sentences, segmented_sentences):
            write_line = "{}\t{}\t{}\n".format(origin, seg, label)
            # print("写入：" + write_line)
            output_file.write(write_line)

    output_file.close()


def seg_file_wp(input_file, output_file, column, label, DS: Dictionnary_Segmentation):
    """
    输入句子文件，输出 用标准词替换并分词 后的文件
    :param input_file: 输入文件
    :param output_file: 输出文件
    :param column: 需要处理的句子所在的列号
    :param label: 所有句子的标签（目前的需求全是正例，故标签统一，需求变化时要考虑修改）
    :param DS: Dictionnary_Segmentation 对象，用于替换和分词
    :return: null
    """
    # 输入句子去重
    txtlines = list(set(open(input_file, "r+", encoding='utf-8').readlines()))
    output_file = open(output_file, 'w+', encoding='utf-8')

    original_sentences = []
    for txtline in txtlines:
        original_sentences.append(txtline.replace('\n', '').split('\t')[column-1])
    segmented_sentences = seg_memlist_wp(original_sentences, DS)
    for origin, seg in zip(original_sentences, segmented_sentences):
            write_line = "{}\t{}\t{}\n".format(origin, seg, label)
            # print("写入：" + write_line)
            output_file.write(write_line)

    output_file.close()


if __name__ == "__main__":

    sentences = ["汽车贷款怎么还款", "车贷如何申请", "车贷如何还款"]
    Custom_Dictionary_File = './dictionary/Custom_Dictionary.txt'  # 自定义词典
    Similar_Dictionary_File = './dictionary/Similar_Dictionary.txt'  # 相似问词典
    Keyword_Dictionary_File = './dictionary/Keyword_Dictionary.txt'
    DS = Dictionnary_Segmentation(Custom_Dictionary_File, Similar_Dictionary_File)
    # DS.initialize_keyword_dictionary(Keyword_Dictionary_File)

    input_file = './input.txt'
    output_file_seg = './input_seg.txt'
    output_file_wp = './input_wp.txt'
    output_file_seg_wp = './input_seg_wp.txt'

    column = 2
    label = '1'
    seg_file(input_file, output_file_seg, column, label, DS)
    wp_file(input_file, output_file_wp, column, label, DS)
    seg_file_wp(input_file, output_file_seg_wp, column, label, DS)
