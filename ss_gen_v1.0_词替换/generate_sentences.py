#!/usr/bin/env python
# coding: utf-8

import time
from word_replace import replace
from sentence_translate import translate
from segmentation import Dictionnary_Segmentation


def generate(
        original_sentence: str,
        DS: Dictionnary_Segmentation,
        synonymous=True,
        trans=True
) -> list:
    """
    输入一个句子，输出句子的相似句列表

    :param original_sentence: str, 原句
    :param similar_dict_file: str, 同义词字典文件
    :param custom_dict_file: str, 自定义字典文件
    :param synonymous: bool, 是否使用同义词替换功能
    :param trans: bool, 是否为每一句生成单独的相似句文件，以原句作为文件名
    :return: list, 原句的相似句列表
    """

    replaced_sentences = []
    translated_sentences = []

    if synonymous:
        replaced_sentences = replace(original_sentence, DS)
    if trans:
        language_list = [("zh", "en"), ("zh", "de"), ("zh", "jp")]
        for lang_pair in language_list:
            source_lang = lang_pair[0]
            target_lang = lang_pair[1]
            time.sleep(1)
            # 翻译： 中文 -> 外文 -> 中文
            intermediate = translate(original_sentence, source_lang, target_lang)
            time.sleep(1)
            translated = translate(intermediate, target_lang, source_lang)
            print("翻译后：{}".format(translated))
            translated_sentences.append(translated)

    result = replaced_sentences + translated_sentences
    return result


def generate_similar_sentences(
        input_file,
        output_file,
        column,
        label,
        custom_dict_file,
        similar_dict_file,
        single_file_output=False
):
    """
    输入一个句子文件，输出包含相似句的文件

    :param original_sentence: 原句
    :param column: 原句在文件中的列号
    :param label: 生成句子的标签
    :param similar_dict_file: 同义词字典文件
    :param custom_dict_file: 自定义字典文件
    :param output_file: 输出文件
    :param single_file_output: 是否为每一句生成单独的相似句文件，以原句作为文件名
    :return: 生成一个 output_file 文件, 第一列为原句，第二列为生成的相似句，第三列为标签
    """

    # 去掉输入中重复的句子
    txtlines = list(set(open(input_file, "r+", encoding='utf-8').readlines()))
    output_file = open(output_file, 'w+', encoding='utf-8')
    DS = Dictionnary_Segmentation(custom_dict_file, similar_dict_file)
    for txtline in txtlines:
        original_sentence = txtline.replace('\n', '').split('\t')[column-1]
        similar_sentences = list(set(generate(original_sentence, DS)))
        for generated_sentence in similar_sentences:
            output_file.write("{}\t{}\t{}\n".format(original_sentence, generated_sentence, label))

    output_file.close()


if __name__ == "__main__":
    input_filename = 'input.txt'
    output_filename = 'input_wp.txt'
    Custom_Dictionary_File = './dictionary/Custom_Dictionary_v1.1.txt'  # 自定义词典
    Similar_Dictionary_File = './dictionary/Similar_Dictionary_v1.1.txt'  # 相似词词典
    column = 2  # 关键词句在文件中所在的列数
    label = '1' # 句子标签

    generate_similar_sentences(
        input_filename,
        output_filename,
        column,
        label,
        Custom_Dictionary_File,
        Similar_Dictionary_File,
    )
    # sentence = "车贷怎么还"
    # result = generate(sentence, Custom_Dictionary_File, Similar_Dictionary_File)
    # for sen in result:
    #     print(sen+'\n')