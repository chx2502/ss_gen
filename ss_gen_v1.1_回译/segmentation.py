#!/usr/bin/env python
# coding: utf-8


from pyhanlp import *
import copy


class Dictionnary_Segmentation():
    def __init__(self, Custom_Dictionnary, Similar_Dictionary):
        self.CustomDictionary = self.genCustomDictionary(Custom_Dictionnary)
        self.initialize_similar_dictionary(Similar_Dictionary)
        self.initialize_similar_vocabulary(Similar_Dictionary)  # 同义词表初始化
        self.keywords = []


    def genCustomDictionary(self, Custom_Dictionnary_File):
        CustomDictionary = LazyLoadingJClass('com.hankcs.hanlp.dictionary.CustomDictionary')
        Custom_Dictionnary_Words = open(Custom_Dictionnary_File, 'r', encoding='utf-8').readlines()
        for word in Custom_Dictionnary_Words:
            CustomDictionary.add(word.replace('\n', ''))
        return CustomDictionary


    def initialize_similar_dictionary(self, Similar_Dictionary_File):
        self.similar_dictionary = dict()
        similar_lines = open(Similar_Dictionary_File, 'r+', encoding='utf-8').readlines()
        for line in similar_lines:
            wordlist = line.replace('\n', '').split('\t')
            for i in wordlist[1:]:
                self.similar_dictionary.setdefault(i, wordlist[0])


    # 对存在同义词的 word 以 word 为 key 构造字典
    # 将整行相似词生成的 list 作为该行每个词的 value，以便替换
    # 大部分过程与 initialize_similar_dictionary 重复，会导致读取两次同义词文件

    def initialize_similar_vocabulary(self, Similar_Dictionary_File):
        self.similar_vocabulary = dict()
        similar_lines = open(Similar_Dictionary_File, 'r+', encoding='utf-8').readlines()
        for line in similar_lines:
            wordlist = line.replace('\n', '').split('\t')
            for word in wordlist:
                self.similar_vocabulary.setdefault(word, wordlist)


    # def initialize_similar_dictionary(self, Similar_Dictionary_File):
    #     # 对存在同义词的 word 以 word 为 key 构造字典
    #     self.similar_dictionary = dict()
    #     similar_lines = open(Similar_Dictionary_File, 'r+', encoding='utf-8').readlines()
    #     for line in similar_lines:
    #         wordlist = line.replace('\n', '').split('\t')
    #         # 将整行相似词生成的 list 作为该行每个词的 value，以便替换
    #         for word in wordlist:
    #             self.similar_dictionary.setdefault(word, wordlist)


    def initialize_keyword_dictionary(self, Keyword_Dictionary_File):
        keyword_lines = open(Keyword_Dictionary_File, 'r+', encoding='utf-8').readlines()
        for keyword in keyword_lines:
            self.keywords.append(keyword.replace('\n', ''))


    def Query_CustomDictionary_Recognize(self, sentence_str):
        wordlist = HanLP.segment(sentence_str)
        line_after_recognize = ""
        for split_word in wordlist:
            word = str(split_word).split('/')[-2]
            if word in self.similar_dictionary:
                similar_word = self.similar_dictionary[word]
            else:
                similar_word = word
            if similar_word in self.keywords:
                line_after_recognize += similar_word
        return line_after_recognize


    def CustomDictionary_Segmentation(self, sentence_str):
        word_list = []
        wordlist = HanLP.segment(sentence_str)
        for word in wordlist:
            word_list.append(self.similar_word(str(word).split('/')[-2]))
        return word_list


    # def CustomDictionary_Segmentation(self, sentence_str):
    #     word_list = []
    #     wordlist = HanLP.segment(sentence_str)
    #     for word in wordlist:
    #         similar_list = self.similar_word(str(word).split('/')[-2])
    #         word_list.append(similar_list[0])
    #     return word_list


    def CustomDictionary_Recognize(self, sentence_str):
        wordlist = HanLP.segment(sentence_str)
        line_after_recognize = ""
        for word in wordlist:
            line_after_recognize += self.similar_word(str(word).split('/')[-2])
        return line_after_recognize


    def segmentation_without_replace(self, sentence_str):
        result = []
        wordlist = HanLP.segment(sentence_str)
        for word in wordlist:
            result.append(str(word).split('/')[-2])
        return result



    def similar_word(self, word):
        if word in self.similar_dictionary:
            return self.similar_dictionary[word]
        else:
            return word


    # def similar_word(self, word):
    #     """
    #     :param word: str, 句子中的词
    #     :return: list, 同义词列表
    #     """
    #     if word in self.similar_dictionary:
    #         return self.similar_dictionary[word]
    #     else:
    #         return list(word)

    def get_similar_vocabulary(self, word):
        if word in self.similar_vocabulary:
            return self.similar_vocabulary[word]
        else:
            return list(word)


    # 用 CustomDictionary 分词并用 SimilarDictionary 替换同义词
    def generate_similar_sentences(self, sentence_str):
        word_list = []
        word_list = HanLP.segment(sentence_str)
        sentences_list = []
        original_sentence = []

        for element in word_list:
            word = str(element).split('/')[-2]
            original_sentence.append(word)

        sentences_list.append(original_sentence)

        # 对原句子中的每个词逐个替换
        for i in range(0, len(original_sentence)):
            word = original_sentence[i]

            # 检查当前第 i 个词能否替换
            if word in self.similar_vocabulary:
                print("开始替换:" + str(original_sentence))
                similar_list = self.get_similar_vocabulary(word)
                print("相似词:" + str(similar_list))

                # 当前第 i 个词可替换，则对 sentences_list 中每个句子的第 i 个词进行替换
                # 新生成的句子会加入 sentences_list 中，所以要先保存生成前的句子数
                curr_sentences_num = len(sentences_list)
                for j in range(0, curr_sentences_num):
                    sentence = sentences_list[j]
                    for similar_word in similar_list:
                        if sentence[i] != similar_word:
                            new_sentence = copy.deepcopy(sentence)
                            new_sentence[i] = similar_word
                            print("替换后:" + ''.join(new_sentence))
                            sentences_list.append(new_sentence)

        return sentences_list

        

