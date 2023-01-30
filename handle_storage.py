import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("firebase_secret.json")
firebase_admin.initialize_app(cred, {
	'storageBucket':'diabetic-retinopathy-1b779.appspot.com'
	})
bucket = storage.bucket()
# filename='jayant_image.jpg'
# blob=bucket.blob(filename)
# blob.upload_from_filename('./jayant_image.jpg')

# blob.download_to_filename('result_')

def upload_image(filepath):
	ans=None
	try:
		with bucket.blob(filepath) as blob:
			blob.upload_from_filename(filepath)
		print('Upload done for :',filepath)
		ans=True
	except Exception as e:
		print(e)
		print('Problem occured while uploading')
		ans=False
	finally:
		return ans

def download_image(filename,type):
	ans=None
	try:
		with bucket.blob(filename) as blob:
			blob.down_to_filename('result_'+type+'.jpg')
		print('Download of image done')
		ans=True
	except Exception as e:
		print(e)
		print('Problem occured while downloading')
		ans=False
	finally:
		return ans

