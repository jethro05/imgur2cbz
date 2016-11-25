import os
import sys
import urllib.request
from imgurpython import ImgurClient
import zipfile

def zipdir(path, ziph):
	for root, dirs, files in os.walk(path):
		for file in files:
			ziph.write(os.path.join(root, file))


album_id = sys.argv[1]

client_id = 'a17235ad4b51446'
client_secret = '66b1c6fc9c7ffd4b665ea7ba9cb6beb67a4d47c7'

client = ImgurClient(client_id, client_secret)

album = client.get_album(album_id)

album_dir = '%s - %s' % (album.id, album.title)
os.mkdir(album_dir)

seq = 0
for image in album.images:
	seq += 1
	therest, filename = image['link'].rsplit('/', 1)
	filename,extension = filename.rsplit('.', 1)
	urllib.request.urlretrieve(image['link'], "%s/%04d.%s" % (album_dir, seq, extension))
	print(("%0"+ str(len(str(len(album.images)))) +"d/%d") % (seq, len(album.images)), image['link'])

zipf = zipfile.ZipFile("%s.cbz" % album_dir, 'w', zipfile.ZIP_STORED)
zipdir("%s/" % album_dir, zipf)
zipf.close()




