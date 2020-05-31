#!/usr/bin/env python
# coding: utf-8

from segmentation import Dictionnary_Segmentation

<<<<<<< Updated upstream

def generate_similar_sentences(
        txtfile,
        column,
        label,
        custom_dict_file,
        similar_dict_file,
        output_file,
        single_file_output=False,
):
    """
    :param txtfile: 要生成同义句的句子文件
    :param column: 原句在文件中的列号
    :param label: 生成句子的标签
    :param similar_dict_file: 同义词字典文件
    :param custom_dict_file: 自定义字典文件
    :param output_file: 输出文件
    :param single_file_output: 是否为每一句生成单独的相似句文件，以原句作为文件名
    :return: 生成一个 output_file 文件, 第一列为原句，第二列为生成的相似句，第三列为标签
    """

    DS = Dictionnary_Segmentation(custom_dict_file, similar_dict_file)
    txtlines = open(txtfile, "r+", encoding='utf-8').readlines()
    output_file = open(output_file, 'w+', encoding='utf-8')
    
    for txtline in txtlines:
        original_sentence = txtline.replace('\n', '').split('\t')[column-1]
        similar_sentences_list = DS.Generate_Similar_Sentences(original_sentence)

        if single_file_output:
            single_sentence_output = open('{}.txt'.format(original_sentence), 'w+', encoding='utf-8')
            single_sentence_output.write("{}\t{}\n".format(original_sentence, label))

        if len(similar_sentences_list) > 1:
            for i in range(1, len(similar_sentences_list)):
                similar_sentence = ''.join(similar_sentences_list[i])
                output_file.write("{}\t{}\t{}\n".format(original_sentence, similar_sentence, label))
                if single_file_output:
                    single_sentence_output.write("{}\t{}\n".format(similar_sentence, label))
=======
def replace(original_sentence: str, DS: Dictionnary_Segmentation) -> list :

    result = []
    # 调用 Dictionnary_Segmentation 类中的 Generate_Similar_Sentences 方法实现 分词 + 同义词替换
    similar_sentences_list = DS.generate_similar_sentences(original_sentence)
    if len(similar_sentences_list) > 1:
        for i in range(1, len(similar_sentences_list)):
            similar_sentence = ''.join(similar_sentences_list[i])
            result.append(similar_sentence)
    else:
        print("句子未命中同义词：{}".format(original_sentence))
        result.append(original_sentence)
>>>>>>> Stashed changes

    output_file.close()


<<<<<<< Updated upstream
if __name__ == "__main__":
    input_filename = 'input.txt'
    output_filename = 'input_wp.txt'
    label = '1'
    Custom_Dictionary_File = './Custom_Dictionary_v1.1.txt'  # 自定义词典
    Similar_Dictionary_File = './Similar_Dictionary_v1.1.txt'  # 相似问词典

    column = 2  # 关键词句在文件中所在的列数
    generate_similar_sentences(
        input_filename,
        column,
        label,
        Custom_Dictionary_File,
        Similar_Dictionary_File,
        output_filename
    )

=======
if __name__ == '__main__':
    sentence = "车贷怎么还款"
    Custom_Dictionary_File = './dictionary/Custom_Dictionary_v1.1.txt'  # 自定义词典
    Similar_Dictionary_File = './dictionary/Similar_Dictionary_v1.1.txt'  # 相似问词典
    DS = Dictionnary_Segmentation(Custom_Dictionary_File, Similar_Dictionary_File)
    result = replace(sentence, DS)
    print(result)
>>>>>>> Stashed changes
