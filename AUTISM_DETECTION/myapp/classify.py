import tensorflow as tf
import sys
import os


# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

# image_path = sys.argv[1]
image_path=""


def check(path):
    image_data = tf.io.gfile.GFile(path, 'rb').read()

    label_lines = [line.rstrip() for line in
                   tf.io.gfile.GFile(
                       r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\static\output_labels.txt"
                   )]

    with tf.compat.v1.gfile.FastGFile(
        r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\static\output_graph.pb", 'rb'
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

    # 🔹 Autism decision logic
    autism_yes = ['combined', 'hyperactive', 'inattentive']

    if predicted_label.lower() in autism_yes:
        autism_result = "YES"
    else:
        autism_result = "NO"

    return {
        "label": predicted_label,
        "confidence": confidence,
        "autism": autism_result
    }



# Read the image_data
# def check(path):
#     # image_data = tf.gfile.FastGFile("C:\\Users\\asus\\Pictures\\new topics\\images\\ceviche\\2591769.jpg", 'rb').read()
#     image_data = tf.io.gfile.GFile(path, 'rb').read()
#
#
#     # Loads label file, strips off carriage return
#     label_lines = [line.rstrip() for line
#                        in tf.io.gfile.GFile(r"C:\Users\Acer\PycharmProjects\AUTISM_DETECTION\myapp\static\output_labels.txt")]
#
#     # Unpersists graph from file
#     with tf.compat.v1.gfile.FastGFile(r"C:\Users\Acer\PycharmProjects\AUTISM_DETECTION\myapp\static\output_graph.pb", 'rb') as f:
#         graph_def = tf.compat.v1.GraphDef()
#         graph_def.ParseFromString(f.read())
#         _ = tf.import_graph_def(graph_def, name='')
#
#     with tf.compat.v1.Session() as sess:
#         # Feed the image_data as input to the graph and get first prediction
#         softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
#
#         predictions = sess.run(softmax_tensor, \
#                  {'DecodeJpeg/contents:0': image_data})
#
#         # Sort to show labels of first prediction in order of confidence
#         top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
#         # print(top_k)
#         for node_id in top_k:
#             human_string = label_lines[node_id]
#             score = predictions[0][node_id]
#             print('%s (score = %.5f)' % (human_string, score))
#     nid=top_k[0]
#     print(label_lines[nid],predictions[0][nid])
#     return label_lines[nid],predictions[0][nid]
# # check(r"D:\ADHD\dataset\ADHD-Inattentive\qc_fdc8dd68e5fe4648b89d2dba2d5e7092.gif")