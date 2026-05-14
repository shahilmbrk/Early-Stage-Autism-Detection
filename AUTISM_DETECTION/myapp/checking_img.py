import tensorflow as tf
import sys
import os


# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

# image_path = sys.argv[1]
image_path=""


def check_type(path):
    image_data = tf.io.gfile.GFile(path, 'rb').read()

    label_lines = [line.rstrip() for line in
                   tf.io.gfile.GFile(
                       r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\type\output_labels.txt"
                   )]

    with tf.compat.v1.gfile.FastGFile(
        r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\type\output_graph.pb", 'rb'
    ) as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    with tf.compat.v1.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(
            softmax_tensor,
            {'DecodeJpeg/contents:0': image_data}
        )

        top_k = predictions[0].argsort()[::-1]
        nid = top_k[0]

        predicted_label = label_lines[nid]
        confidence = float(predictions[0][nid])



    return predicted_label,confidence


# print(check_type(r"C:\Users\USER\Downloads\audio new.png"))