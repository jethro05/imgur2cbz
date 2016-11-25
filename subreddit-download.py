import os
import sys
import urllib.request
from imgurpython import ImgurClient
import zipfile
import praw
import shutil


client_id= 'a17235ad4b51446'
client_secret = '66b1c6fc9c7ffd4b665ea7ba9cb6beb67a4d47c7'

client = ImgurClient(client_id, client_secret)

def zipdir(path, ziph):
	for root, dirs, files in os.walk(path):
		for file in files:
			ziph.write(os.path.join(root, file))




subreddit = sys.argv[1]
r = praw.Reddit(user_agent="imgur2cbz")
submissions = r.get_subreddit(subreddit).get_hot(limit=100)

for x in submissions:
	if 'imgur' not in x.url:
		continue;

	path_rest, album_id = x.url.rsplit('/', 1)
	album = client.get_album(album_id)

	album_dir = '%s/%s - %s' % (subreddit, album.id, album.title)
	try:
		os.makedirs(album_dir)
	except Exception as e:
		print(album_dir, "already exists", e)
		continue
	print(album_dir)

	seq = 0
	for image in album.images:
		seq += 1
		therest, filename = image['link'].rsplit('/', 1)
		filename,extension = filename.rsplit('.', 1)
		urllib.request.urlretrieve(image['link'], "%s/%04d.%s" % (album_dir, seq, extension))
		print(("\t%0"+ str(len(str(len(album.images)))) +"d/%d") % (seq, len(album.images)), image['link'])

	zipf = zipfile.ZipFile("%s.cbz" % album_dir, 'w', zipfile.ZIP_STORED)
	zipdir("%s/" % album_dir, zipf)
	zipf.close()




