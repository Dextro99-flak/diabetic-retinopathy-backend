import firebase_admin
from firebase_admin import credentials, storage
from io import BytesIO
cred = credentials.Certificate("firebase_secret.json")
firebase_admin.initialize_app(cred, {
	'storageBucket':'diabetic-retinopathy-1b779.appspot.com'
	})
bucket = storage.bucket()

def upload_image(file_string,filename):
	blob=bucket.blob(filename)
	bb=BytesIO(file_string)
	blob.upload_from_string(bb.read(),content_type='image/jpg')
	return None

def download_image(filename,type):
	blob=bucket.blob(filename)
	print('File to download',filename)
	blob.download_to_filename('result_'+type+'.jpg')
	print('Download of image done')
	ans=True
	return ans

