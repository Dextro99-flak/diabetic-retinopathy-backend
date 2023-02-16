from flask import abort
import config
from imagekitio import ImageKit
import prediction
import handle_storage
from flask import send_file
from imagekitio.models.ListAndSearchFileRequestOptions import ListAndSearchFileRequestOptions
from connexion import request
from PIL import Image
import numpy as np
from io import BytesIO
PRIVATE_KEY = 'private_Dog3OixXj6JG3UPRSjMt2DGniKc='
PUBLIC_KEY = 'public_KKeDUuVKjvcDLawqxtJCmIYmXcI='
URL = 'https://ik.imagekit.io/aqxxdd9fw'
imagekit = ImageKit(
    private_key=PRIVATE_KEY,
    public_key=PUBLIC_KEY,
    url_endpoint=URL
)
'''
Database will be needed that will store the following Tables :
	-> Users and auth_key mapping (Users table)
	-> Image Name to DR Grade Mapping (Grade table) (Image file name will be primary key) (DR Segmentation File Names will also be there)
'''

def check_file(filename):
	return 'A1'
	analyse = config.Analysis.query.filter(config.Analysis.image_filename==filename).one_or_none()
	if analyse==None:
		return None
	else:
		return image_filename

def verify(auth_key):
	if auth_key=='ABCD':
		return True
	else:
		return False

def send_to_cdn(auth_key,patient_id,date):
	if verify(auth_key):
		filename=str(patient_id)+'_'+str(date)+'.jpg'
		n1 = config.Analysis(patient_id=patient_id, image_filename=filename, date_analysed=date)
		config.db.session.add(n1)
		handle_storage.upload_image(request.data,filename)
		config.db.session.commit()
		return {'filename':filename},200
	else:
		abort(401,'wrong auth_key')
		

def get_grade(auth_key,patient_id,date):
	if verify(auth_key):
		patient = config.Analysis.query.filter(config.Analysis.patient_id==patient_id, config.Analysis.date_analysed==date).first()
		print(patient,patient.grade)
		if not patient:
			return {'name':None,'patient_id':None, 'grade':None, 'result':'Wrong Details'},400
		if patient.grade is not None:
			print('SINCE GRADE WAS ALREADY PRESENT I RETURNED WHATEVER WAS GIVEN ALREADY')
			return {'patient_id':patient_id,'grade':patient.grade, 'result':'success'},200
		else:
			print('SINCE GRADE WAS NOT PRESENT I PREDICTED THAT GRADE')
			ans=handle_storage.download_image(patient.image_filename)
			patient.grade=prediction.get_grade(patient.image_filename)
			config.db.session.commit()
			return {'patient_id':patient_id, 'grade':patient.grade, 'result':'success'},200
	else:
		abort(401,'wrong auth_key')

def segment_HE(auth_key,patient_id,date):
	if verify(auth_key):
		patient = config.Analysis.query.filter(config.Analysis.patient_id==patient_id, config.Analysis.date_analysed==date).first()
		if not patient:
			return {'name':None,'patient_id':None, 'he_filename':None, 'result':'Wrong Details'},400
		if patient.he_filename:
			print('SINCE HAEMORRHAGE WAS ALREADY SEGMENTED I RETURNED WHATEVER IMAGE WAS ALREADY THERE')
			ans=handle_storage.download_image(patient.he_filename)
			return send_file(patient.he_filename, mimetype='image/jpg')
			#return {'name':img_name,'patient_id':patient_id, 'he_filename':patient.he_filename, 'result':'success'},200
		else:
			print('SINCE HAEMORRHAGE WAS NOT SEGMENTED I SEGMENTED IT AND RETURNED')
			# Code for extracting the image from firebase
			# Code for calling the module that will perform the segmentation
			# Code for uploading image to firebase
			# name of image will be : image_filename+haemorrhage_done
			patient.he_filename = patient.patient_id+'_'+date+'_'+'_haemorrhage_done.jpg'
			ans=handle_storage.download_image(patient.image_filename)
			pred_img=prediction.get_full_segmented_haemorrhage(patient.image_filename)
			img=Image.fromarray(np.uint8(pred_img))
			buff=BytesIO()
			img.save(buff, format='JPEG')
			img=buff.getvalue()
			print('the type of image being handled is : ',type(img))
			abss=handle_storage.upload_image(img,patient.he_filename)
			config.db.session.commit()
			ans=handle_storage.download_image(patient.he_filename)
			return send_file(patient.he_filename, mimetype='image/jpg')
			#return {'name':img_name,'patient_id':patient_id, 'he_filename':patient.he_filename, 'result':'success'},200
	else:
		abort(404,'wrong auth_key')



def segment_EX(auth_key,patient_id,date):
	if verify(auth_key):
		patient = config.Analysis.query.filter(config.Analysis.patient_id==patient_id, config.Analysis.date_analysed==date).first()
		if not patient:
			return {'name':None,'patient_id':None, 'ex_filename':None, 'result':'Wrong Details'},400
		if patient.ex_filename:
			print('SINCE HARD EXUDATE WAS ALREADY SEGMENTED I RETURNED WHATEVER IMAGE WAS ALREADY THERE')
			ans=handle_storage.download_image(patient.ex_filename)
			# img=Image.open(patient.ex_filename)
			# im1=np.asarray(img)
			# buff=BytesIO()
			# img.save(buff, format='JPEG')
			# img=buff.getvalue()
			return send_file(patient.ex_filename, mimetype='image/jpg')
			#return {'patient_id':patient_id, 'ex_file':str(img), 'result':'success', 'image_shape':im1.shape},200
		else:
			print('SINCE HARD EXUDATE WAS NOT SEGMENTED I SEGMENTED IT AND RETURNED')
			# Code for extracting the image from firebase
			# Code for calling the module that will perform the segmentation
			# Code for uploading image to firebase
			# name of image will be : patient_id+hard_exudate_done
			patient.ex_filename = patient.patient_id+'_'+date+'_'+'_hard_exudate_done.jpg'
			ans=handle_storage.download_image(patient.image_filename)
			pred_img=prediction.get_full_segmented_hard_exudate(patient.image_filename)
			img=Image.fromarray(np.uint8(pred_img))
			buff=BytesIO()
			img.save(buff, format='JPEG')
			img=buff.getvalue()
			print('the type of image being handled is : ',type(img))
			abss=handle_storage.upload_image(img,patient.ex_filename)
			config.db.session.commit()
			ans=handle_storage.download_image(patient.ex_filename)
			return send_file(patient.he_filename, mimetype='image/jpg')
			#return {'patient_id':patient_id, 'ex_file':str(img), 'result':'success', 'image_shape':pred_img.shape},200
	else:
		abort(404,'wrong auth_key')

def segment_SE(auth_key,patient_id,date):
	if verify(auth_key):
		patient = config.Analysis.query.filter(config.Analysis.patient_id==patient_id, config.Analysis.date_analysed==date).first()
		if not patient:
			return {'name':None,'patient_id':None, 'se_filename':None, 'result':'Wrong Details'},400
		if patient.se_filename:
			print('SINCE SOFT EXUDATE WAS ALREADY SEGMENTED I RETURNED WHATEVER IMAGE WAS ALREADY THERE')
			ans=handle_storage.download_image(patient.se_filename)
			return send_file(patient.se_filename, mimetype='image/jpg')
			#return {'name':img_name,'patient_id':patient_id, 'se_filename':patient.se_filename, 'result':'success'},200
		else:
			print('SINCE SOFT EXUDATE WAS NOT SEGMENTED I SEGMENTED IT AND RETURNED')
			# Code for extracting the image from firebase
			# Code for calling the module that will perform the segmentation
			# Code for uploading image to firebase
			# name of image will be : image_filename+soft_exudate_done
			patient.se_filename = patient.patient_id+'_'+date+'_'+'_soft_exudate_done.jpg'
			ans=handle_storage.download_image(patient.image_filename)
			pred_img=prediction.get_full_segmented_soft_exudate(patient.image_filename)
			img=Image.fromarray(np.uint8(pred_img))
			buff=BytesIO()
			img.save(buff, format='JPEG')
			img=buff.getvalue()
			print('the type of image being handled is : ',type(img))
			abss=handle_storage.upload_image(img,patient.se_filename)
			config.db.session.commit()
			ans=handle_storage.download_image(patient.se_filename)
			return send_file(patient.se_filename)
			#return {'name':img_name,'patient_id':patient_id, 'se_filename':patient.se_filename, 'result':'success'},200
	else:
		abort(404,'wrong auth_key')


def segment_MA(auth_key,patient_id,date):
	if verify(auth_key):
		patient = config.Analysis.query.filter(config.Analysis.patient_id==patient_id, config.Analysis.date_analysed==date).first()
		if not patient:
			return {'name':None,'patient_id':None, 'ma_filename':None, 'result':'Wrong Details'},400
		if patient.ma_filename:
			print('SINCE MICRO ANEURYSM WAS ALREADY SEGMENTED I RETURNED WHATEVER IMAGE WAS ALREADY THERE')
			ans=handle_storage.download_image(patient.ma_filename)
			return send_file(patient.ma_filename)
			#return {'name':img_name,'patient_id':patient_id, 'ma_filename':patient.ma_filename, 'result':'success'},200
		else:
			print('SINCE MICRO ANEURYSM WAS NOT SEGMENTED I SEGMENTED IT AND RETURNED')
			# Code for extracting the image from firebase
			# Code for calling the module that will perform the segmentation
			# Code for uploading image to firebase
			# name of image will be : image_filename+soft_exudate_done
			patient.ma_filename = patient.patient_id+'micro_aneurysm_done.jpg'
			ans=handle_storage.download_image(patient.image_filename)
			pred_img=prediction.get_full_segmented_micro_aneurysm(patient.image_filename)
			img=Image.fromarray(np.uint8(pred_img))
			buff=BytesIO()
			img.save(buff, format='JPEG')
			img=buff.getvalue()
			print('the type of image being handled is : ',type(img))
			abss=handle_storage.upload_image(img,patient.ma_filename)
			config.db.session.commit()
			ans=handle_storage.download_image(patient.ma_filename)
			return send_file(patient.ma_filename, mimetype='image/jpg')
			#return {'name':img_name,'patient_id':patient_id, 'se_filename':patient.se_filename, 'result':'success'},200
	else:
		abort(404,'wrong auth_key')