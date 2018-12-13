import jieba
from gensim import corpora, models, similarities
from word2vec import W2V
import numpy as np
import codecs
import os
import tensorflow as tf
import rnncell as rnn
from tensorflow.contrib.layers.python.layers import initializers


# 得到预训练的词表，作为全局变量。只需要获得一次之后便可以一直使用。提高效率
dict = W2V.our_get_embeddings()


# 对输入的两个文本进行分词
def tokenization(str1, str2):
    str1 = str1.replace(' ', ',').replace('\t', ',').replace('\u3000', ',')
    str2 = str2.replace(' ', ',').replace('\t', ',').replace('\u3000', ',')

    str1_seg = jieba.cut(str1)
    res_str1 = " ".join(str1_seg).split(" ")

    str2_seg = jieba.cut(str2)
    res_str2 = " ".join(str2_seg).split(" ")
    return res_str1, res_str2


# 得到输入和输出的向量表示

def get_vectors(str_in, str_out):
    list_in, list_out = tokenization(str_in, str_out)
    vec_in = [0] * 32
    vec_out = [0] * 32
    for item in list_in:
        vec_in = [a+b for a, b in zip(vec_in, dict[item])]
    vec_in = [v/len(list_in) for v in vec_in]

    for item in list_out:
        vec_out = [a+b for a, b in zip(vec_out, dict[item])]
    vec_out = [v/len(list_out) for v in vec_out]
    # print(1111111111, vec_in)
    # print(222222222, vec_out)
    # print(3333333333, list_in)
    # print(4444444444, list_out)
    return vec_in, vec_out


# def get_vectors(str_in, str_out):
#     list_in, list_out = tokenization(str_in, str_out)
#     vec_in = []
#
#     for item in list_in:
#         vec_in.append(dict[item])
#
#     return vec_in


# 引入BiLSTM层来再次处理加和求平均之后的向量表示
def biLSTM_layer(inputs, lstm_dim, lengths, name=None):
    """
    :param lstm_inputs: [batch_size, num_steps, emb_size]
    :return: [batch_size, num_steps, 2*lstm_dim]
    """
    initializer = initializers.xavier_initializer()
    # sess = tf.Session()
    # sess.run(tf.global_variables_initializer())
    with tf.variable_scope("BiLSTM_Layer" if not name else name):
        lstm_cell = {}
        for direction in ["forward", "backward"]:
            with tf.variable_scope(direction):
                lstm_cell[direction] = rnn.CoupledInputForgetGateLSTMCell(
                    lstm_dim,
                    use_peepholes=True,
                    initializer=initializer,
                    state_is_tuple=True)
        outputs, final_states = tf.nn.bidirectional_dynamic_rnn(
            lstm_cell["forward"],
            lstm_cell["backward"],
            inputs,
            dtype=tf.float32,
            sequence_length=lengths)
    return tf.concat(outputs, axis=2)


def biLSTM_layer_2(inputs, lstm_dim, lengths, name=None):
    """
    :param lstm_inputs: [batch_size, num_steps, emb_size]
    :return: [batch_size, num_steps, 2*lstm_dim]
    """
    initializer = initializers.xavier_initializer()
    # sess = tf.Session()
    # sess.run(tf.global_variables_initializer())
    with tf.variable_scope("BiLSTM" if not name else name):
        lstm_cell = {}
        for direction in ["forward", "backward"]:
            with tf.variable_scope(direction):
                lstm_cell[direction] = rnn.CoupledInputForgetGateLSTMCell(
                    lstm_dim,
                    use_peepholes=True,
                    initializer=initializer,
                    state_is_tuple=True)
        outputs, final_states = tf.nn.bidirectional_dynamic_rnn(
            lstm_cell["forward"],
            lstm_cell["backward"],
            inputs,
            dtype=tf.float32,
            sequence_length=lengths)
    return tf.concat(outputs, axis=2)


# 计算两个文本的相似度
def cos_sim(vec_in, vec_out):
    num = float(np.matrix(vec_in) * np.matrix(vec_out).T)
    denom = np.linalg.norm(vec_in) * np.linalg.norm(vec_out)
    cos = num / denom # 计算cos的方法
    sim = 0.5 + 0.5 * cos  # 对最后算出来的cos进行归一化，使它们位于0-1之间
    print(sim)
    return sim


# 计算全体样本输入输出的相似性
def total_data_sim():
    path = os.getcwd()
    file_in = codecs.open(path + '\dataset\数据集.csv', 'r', encoding='utf-8')
    file_out = codecs.open(path + '\dataset\输入输出相似度.txt', 'w', encoding='utf-8')

    str_in_list = []
    str_out_list = []
    for line in file_in:
        line = line.strip()
        str_in_list.append(line.split(' @ ')[0])
        str_out_list.append(line.split(' @ ')[1])
    for index in range(len(str_in_list)):
        vec_in, vec_out = get_vectors(str_in_list[index], str_out_list[index])
        sim = cos_sim(vec_in, vec_out)
        file_out.write(str_in_list[index].replace('\t', ',') + ' @ ' + str_out_list[index] + '\t' + str(sim) + '\n')
    file_in.close()
    file_out.close()


def analysis_sim():
    path = os.getcwd()
    file_in = codecs.open(path + '\dataset\输入输出相似度.txt', 'r', encoding='utf-8')
    file_out = codecs.open(path + '\dataset\排序_输入输出相似度.txt', 'w', encoding='utf-8')

    dic = {}
    count_lines = 0
    dup = 0
    for line in file_in:
        count_lines += 1
        line = line.strip()
        if line.split('\t')[0] in dic.keys():
            if line.split('\t')[1] == dic[line.split('\t')[0]]:
                dup += 1
        dic[line.split('\t')[0]] = line.split('\t')[1]
    print("输入输出相似度总条数：", count_lines)
    print('文本和相似度整体去重后的数据条数：', len(dic))
    print('文本和相似度都相同的样本的个数：', dup)

    sort_code = sorted(dic.items(), key=lambda d: d[1], reverse=True)
    for item in sort_code:
        file_out.write(item[0] + ' ### ' + item[1] + '\n')
    file_in.close()
    file_out.close()

# *******************************得到加和求平均方法计算出来的相似性
# vec_in, vec_out = get_vectors('心力衰竭,心脏增大', '心脏肥大')
# vec_in, vec_out = get_vectors('衰老', '衰老')
# cos_sim(vec_in, vec_out)
# total_data_sim()
# analysis_sim()


# *******************************得到加入了BiLSTM模型的方法计算出来的相似性
vec_in, vec_out = get_vectors('肺癌,家属代述来院10分钟前在家中发现患者意识丧失呼之不应、立即送来我院就诊。入院时生命体征消失，心电图提示心室停搏，报临床死亡', '支气管和肺恶性肿瘤')
# vec_in, vec_out = get_vectors('心力衰竭,心脏增大', '心脏肥大')
print(type(vec_in))
print(type(vec_out))
#
vec_in = tf.convert_to_tensor(np.asarray(vec_in), dtype=tf.float32)
vec_in = tf.reshape(vec_in, [1,1,32])
vec_out = tf.convert_to_tensor(np.asarray(vec_out), dtype=tf.float32)
vec_out = tf.reshape(vec_out, [1,1,32])
#
# print(type(vec_in))
# print(type(vec_out))
a = biLSTM_layer(vec_in, 32, [1])
print(22222222222, a.shape)
a = tf.reshape(a, [1, -1])
print(1111111111, a.shape)

b = biLSTM_layer_2(vec_out, 32, [1])
b = tf.reshape(b, [1, -1])
# with tf.Session() as sess:
#     sess.run(tf.global_variables_initializer())
#     a = a.eval(session=sess)
#     b = b.eval(session=sess)
# sim = cos_sim(a, b)
with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    dis = sess.run(tf.square(a - b))
    dis1 = sess.run(tf.reduce_sum(tf.square(a - b)))
    tmp = tf.sqrt(tf.reduce_sum(tf.square(a - b)))

    euclidean = sess.run(0.5 + 0.5 * tmp) / 2

print(euclidean)
