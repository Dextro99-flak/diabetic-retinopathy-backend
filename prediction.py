import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
def get_grade(img_filename):
    img=Image.open(img_filename)
    img=np.asarray(img)
    print('Now loading the model')
    model = keras.models.load_model('fundus_grading_model.h5')
    print('Model has been loaded')
    ans = model.predict(np.array([img]))
    print('The answer is :',ans)
    return int(np.argmax(ans))

def get_full_segmented_haemorrhage():
	return True

def get_full_segmented_micro_aneurysm():
	return True

def get_full_segmented_soft_exudate():
	return True

def get_full_segmented_hard_exudate():
	return True