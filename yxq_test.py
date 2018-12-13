import tensorflow as tf

t1 = [[[1, 2], [2, 3]], [[4, 4], [5, 3]]]
t2 = [[[7, 4], [8, 4]], [[2, 10], [15, 11]]]
t = tf.concat([t1, t2], axis=0)

sess = tf.Session()
a = sess.run(t)
print(a)