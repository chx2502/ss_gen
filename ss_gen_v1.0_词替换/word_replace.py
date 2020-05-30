# !/usr/bin/python3
# -*-coding: utf8-*-

from segmentation import Dictionnary_Segmentation

def replace(
        original_sentence: str,
        custom_dict_file: str,
        similar_dict_file: str
) -> list :
    DS = Dictionnary_Segmentation(custom_dict_file, similar_dict_file)
    result = []

    similar_sentences_list = DS.Generate_Similar_Sentences(original_sentence)
    if len(similar_sentences_list) > 1:
        for i in range(1, len(similar_sentences_list)):
            similar_sentence = ''.join(similar_sentences_list[i])
            result.append(similar_sentence)
    else:
        result.append(original_sentence)

    return result


if __name__ == '__main__':
    sentence = "你你你你你你你"
    Custom_Dictionary_File = './Custom_Dictionary_v1.1.txt'  # 自定义词典
    Similar_Dictionary_File = './Similar_Dictionary_v1.1.txt'  # 相似问词典
    result = replace(sentence, Custom_Dictionary_File, Similar_Dictionary_File)
    print(result)