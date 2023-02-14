import firebase_admin
from firebase_admin import credentials, storage
from io import BytesIO
cred = credentials.Certificate("firebase_secret.json")
firebase_admin.initialize_app(cred, {
	'storageBucket':'diabetic-retinopathy-1b779.appspot.com'
	})
bucket = storage.bucket()
# filename='jayant_image.jpg'
# blob=bucket.blob(filename)
# blob.upload_from_filename('./jayant_image.jpg')

# blob.download_to_filename('result_')

def upload_image(file_string):
	ans=None
	try:
		with bucket.blob("result_image.jpg") as blob:
			blb=BytesIO(file_string)
			blob.upload_from_filename(blb.read())
		print('Upload done for :',file_string)
		ans=True
	except Exception as e:
		print(e)
		print('Problem occured while uploading')
		ans=False
	finally:
		return ans
	blob=bucket.blob("result_image.jpg")
	bb=BytesIO(file_string)
	blob.upload_from_string(bb.read())

def download_image(filename,type):
	# ans=None
	# try:
	# 	with bucket.blob(filename) as blob:
	# 		blob.download_to_filename('result_'+type+'.jpg')
	# 	print('Download of image done')
	# 	ans=True
	# except Exception as e:
	# 	print(e)
	# 	print('Problem occured while downloading')
	# 	ans=False
	# finally:
	# 	return ans 
	blob=bucket.blob(filename)
	print('File to download',filename)
	blob.download_to_filename('result_'+type+'.jpg')
	print('Download of image done')
	ans=True
	return ans

