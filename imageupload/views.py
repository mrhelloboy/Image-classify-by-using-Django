from django.shortcuts import render
from .form import UploadImageForm
from .models import Image

import os, sys
import tensorflow as tf


def index(request):
    #label = '12345'
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            picture = Image(photo=request.FILES['image'])
            picture.save()


            #if os.path.isfile(picture.photo.url):

            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

            #image_path = picture

            # Read in the image_data
            image_data = tf.gfile.FastGFile(picture.photo.path, 'rb').read()

            # Loads label file, strips off carriage return
            label_lines = [line.rstrip() for line in tf.gfile.GFile("imageupload/retrained_labels.txt")]

            # Unpersists graph from file
            with tf.gfile.FastGFile("imageupload/retrained_graph.pb", 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                tf.import_graph_def(graph_def, name='')

            with tf.Session() as sess:
                # Feed the image_data as input to the graph and get first prediction
                softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

                predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

                # Sort to show labels of first prediction in order of confidence
                top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

                
                label = []
                i = 1
                for node_id in top_k:
                    human_string = label_lines[node_id]
                    score = predictions[0][node_id]
                        #print('%s (score = %.5f)' % (human_string, score))
                    a = (human_string, score)
                    if i < 2:
                        label.append(a)
                        i += 1
                    else:
                        break

            return render(request, 'show.html', {'picture':picture, 'label':label})

    else:
        form = UploadImageForm()

        return render(request, 'index.html', {'form': form})

