import cv2
import numpy as np
def enhance(images):
    #images is a Tensor with dimensions (batch_size,height,width,channles)
    #returns a Tensor of enhanced images of the same shape as input
    images=images.astype('uint8')
    enhanced_images=[]
    for image in images:
        image_bgr=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        detail_enhanced=cv2.detailEnhance(image_bgr,None,200,0.1)
        gray=cv2.cvtColor(detail_enhanced,cv2.COLOR_BGR2GRAY)
        bilateral_filtered = cv2.bilateralFilter(gray,None,10,10,10)
        log_image=np.log(1+(np.power( bilateral_filtered/255,0.2)*255))
        c=255/np.log(1+np.amax( bilateral_filtered))
        illuminated_image=np.power((c*(log_image/255)),(c-1)/10)*255
        hsv_enhanced=cv2.cvtColor(detail_enhanced,cv2.COLOR_BGR2HSV)
        img=illuminated_image.reshape(illuminated_image.shape[0],illuminated_image.shape[1],1).astype('uint8')
        hsv_final=np.concatenate((hsv_enhanced[:,:,:-1],img) ,axis=-1)
        rgb_final=cv2.cvtColor(hsv_final,cv2.COLOR_HSV2RGB)
        enhanced_images.append(rgb_final)
    
    return tf.convert_to_tensor(enhanced_images)
    