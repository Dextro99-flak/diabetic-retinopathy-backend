import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import cv2
def get_grade(img_filename):
    img=Image.open(img_filename)
    img=np.asarray(img)
    img=cv2.resize(img,(224,224))
    print('Now loading the model')
    model = keras.models.load_model('fundus_grading_model.h5')
    print('Model has been loaded') 
    ans = model.predict(np.array([img]))
    print('The answer is :',ans)
    return int(np.argmax(ans))

def get_full_segmented_hard_exudate(img_filename):
	img=Image.open(img_filename)
	img=np.asarray(img)
	img=cv2.resize(img,(512,512))
	model=keras.model.load_model('UNET_Hard_Exudate.h5')
	pred=model.predict(img)
	img[:,:,1]=img[:,:,1]*np.reshape(pred[0],(512,512))
	return img

def get_full_segmented_micro_aneurysm():
	return True

def get_full_segmented_soft_exudate():
	return True

def get_full_segmented_haemorrhage():
	return True