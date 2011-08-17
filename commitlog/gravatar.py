
#http://blog.gravatar.com/2008/01/17/gravatars-in-python-25/
import urllib, hashlib

# Set your variables here
email = "Someone@somewhere.com"
default = "http://www.somewhere.com/homsar.jpg"
size = 40

def get_gravatar(email):
	gravatar_url = "http://www.gravatar.com/avatar.php?"
	gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(email.lower()).hexdigest(), 'default':default, 'size':str(size)})
	return gravatar_url