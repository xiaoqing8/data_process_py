import os
import codecs
import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import numpy as np


def get_w2v_cut():
    f_write_word = open("D:\stage\data_process_系统对照表\word2vec\cut_数据集.txt", "w", encoding="utf-8")
    with open("D:\stage\data_process_系统对照表\word2vec\数据集.csv", "r", encoding="utf-8") as f_test:
        for line in f_test:
            line = line.strip()
            line_list = []
            seg = jieba.cut(line)
            res = " ".join(seg)
            f_write_word.write(res + '\n')
    f_write_word.close()
    f_test.close()


def train_w2v():
    inp = "cut_数据集.txt"
    outp1 = 'cut_数据集.model'
    outp2 = 'cut_数据集.vector'
    # 此处min_count默认为5，在不修改这个参数的情况下如果字典中的词都少于5个字，
    # 就会出现"you must first build vocabulary before training the model"这个问题
    model = Word2Vec(LineSentence(inp), size=32, window=2, min_count=1, iter=10, seed=0)

    model.save(outp1)
    model.wv.save_word2vec_format(outp2, binary=False)


def our_get_embeddings():
    path = os.getcwd()
    word_file = codecs.open('D:\stage\data_process_系统对照表\word2vec\\vec.txt', 'r', encoding='utf-8')
    all_vector = []
    for line in word_file:
        line = line.strip()
        line_split = line.split(" ")

        vector = []
        for value in line_split:
            vector.append(value)
        all_vector.append(vector)
    word_file.close()

    our_vector = np.array(all_vector)

    # print(len(our_vector))

    dict = {}
    for i in range(len(our_vector)):
        our_float_vec = []
        for j in range(1, len(our_vector[0])):
            our_float_vec.append(float(our_vector[i][j]))
        dict[our_vector[i][0]] = our_float_vec

    return dict