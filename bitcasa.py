# Bitcasa Python Class v2 (Still Unofficial) #
# 2013 Michael Thomas (Biscuit Labs) #

# System Imports
import os, sys, json, time
# Requests Imports
import requests
# Multipart Form Encoding
import codecs, mimetypes, sys, uuid
# Multithreading (planned for Uploads, then slowly roll out to other ops - need to discuss)
# http://code.google.com/p/pyloadtools/wiki/CodeTutorialMultiThreading
# from threading import Thread
# Watchdog (for monitoring mirrored folders)
# from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler

# Bitcasa Uploader Class
# Works great for now, but Upload API changes soon.
class BitcasaUploader(object):
	def __init__(self, filename, chunksize=1 << 13):
		self.filename = filename
		self.chunksize = chunksize
		self.totalsize = os.path.getsize(filename)
		self.readsofar = 0
		# Form Multipart
		self.encoder = codecs.getencoder('utf-8')
		self.boundary = uuid.uuid4().hex
		self.content_type = 'multipart/form-data; boundary={}'.format(self.boundary)

	def __iter__(self):
		with open(self.filename, 'rb') as file:
			# Start Multipart
			form_header = str('--'+self.boundary+'\r\nContent-Disposition: form-data; name="file"; filename="'+self.filename+'"\r\nContent-Type: '+'application/octet-stream'+'\r\n\r\n').encode('utf-8')
			yield form_header
			self.time = time.time()
			while True:
				data = file.read(self.chunksize)
				if not data:
					total_time = time.time() - self.time
					sys.stderr.write("\rFinished uploading file: " + self.filename + " (took "+ str(round(total_time,2)) +" seconds)\n")
					# Finish Multipart
					form_footer = str('\r\n--'+self.boundary+'--\r\n').encode('utf-8')
					yield form_footer
					break
				self.readsofar += len(data)
				percent = self.readsofar * 1e2 / self.totalsize
				sys.stderr.write("\rUploading file: " + self.filename + " {percent:3.0f}%".format(percent=percent))
				yield data
	
	def __len__(self):
		return self.totalsize

class BitcasaUploaderFileAdapter(object):
	def __init__(self, iterable):
		self.iterator = iter(iterable)
		self.length = len(iterable)

	def read(self, size=-1): # TBD: add buffer for `len(data) > size` case
		return next(self.iterator, b'')

	def __len__(self):
		return self.length
		
# Bitcasa Main Class
class Bitcasa:
	# URL "Constants"
	bitcasa_api_url = "https://developer.api.bitcasa.com/v1"	
	oauth_redirect_url = ""
	# API Auth/Access
	api_oauth_token = ""
	api_access_token = ""

	# Setup our class
	def __init__ (self, app_client_id, app_client_secret, debug=False, auth_token=None, access_token=None):
		# Make sure we atleast have a Client ID and/or Client Secret
		self.app_client_id = app_client_id
		self.app_client_secret = app_client_secret
		if(self.app_client_id == None):
			raise Exception("You must have a Bitcasa App Client ID to use this module.")
		if(self.app_client_secret == None):
			raise Exception("You must have a Bitcasa App Secret to use this module.")
		# Set Auth Token and/or Access Token
		self.api_oauth_token = auth_token
		self.api_access_token = access_token
		# Print out lots of useful info
		self.debug = debug

	# Get OAuth URL to get Token
	def oauth_url (self):
		return self.bitcasa_api_url + "/oauth2/authenticate?client_id=" + self.app_client_id + "&redirect=" + self.oauth_redirect_url

	# Authenticate & Get Access Token
	def authenticate (self, oauth=None):
		# Set OAuth Token		
		if(oauth != None):
			self.oauth_token = oauth
		if(self.debug):
			print("[Bitcasa] Authenticate OAuth Token: " + self.oauth_token)

		# Make Request for Access Token
		r = requests.get(self.bitcasa_api_url + "/oauth2/access_token?secret=" + self.app_client_secret + "&code=" + self.oauth_token)
		if(self.debug):
			print("[Network] Request: " + self.bitcasa_api_url + "/oauth2/access_token?secret=" + self.app_client_secret + "&code=" + self.oauth_token)		
		if(r.status_code == 200):
			# Success, set in instance & return
			self.api_access_token = r.json()['result']['access_token']
			return self.api_access_token
		else:
			# Error
			# @todo - Better HTTP/Requests Error Handling
			raise Exception(r.json()['error']['code'], r.json()['error']['message'])
	
	# Get User Profile
	def user_profile(self):
		if(self.debug):
			print("[Bitcasa] Fetch User Information")
		# Make Request for User Profile
		r = requests.get(self.bitcasa_api_url + "/user/profile?access_token=" + self.api_access_token)
		if(self.debug):
			print("[Network] Request: " + self.bitcasa_api_url + "/user/profile?access_token=" + self.api_access_token)		
		if(r.status_code == 200):
			# Success, return profile
			return r.json()['result']
		else:
			# Error
			# @todo - Better HTTP/Requests Error Handling
			raise Exception(r.json()['error']['code'], r.json()['error']['message'])

	### Folder Methods ###

	## List Directory Contents
	def dir (self, path = ""):
		if(self.debug):
			print("[Bitcasa] Listing Directory Contents: " + path)
		r = requests.get(self.bitcasa_api_url + "/folders/" + path + "?access_token=" + self.api_access_token)
		if(self.debug):
			print("[Network] Request: " + self.bitcasa_api_url + "/folders/" + path + "?access_token=" + self.api_access_token)
		if(r.status_code == 200):
			# Success
			contents = r.json()['result']['items']
			return contents
		else:
			# Error
			# @todo - Better HTTP/Requests Error Handling
			raise Exception(r.json()['error']['code'], r.json()['error']['message'])

	## Add Folder
	def mkdir (self, path, folder_name):
		if(self.debug):
			print("[Bitcasa] Creating Directory Named: " + folder_name + " in Path: " + path)
		payload = {'folder_name' : folder_name}
		if(self.debug):
			print("[Network] Request: " + self.bitcasa_api_url + "/folders/" + path + "?access_token=" + self.api_access_token)
		r = requests.post(self.bitcasa_api_url + "/folders/" + path + "?access_token=" + self.api_access_token, data=payload)
		if(r.status_code == 200):
			# Make Sure Errors aren't here
			if(r.json()['error'] == None):
				return r.json()['result']['items']
			else:
				raise Exception(r.json()['error']['code'], r.json()['error']['message'])
		else:
			raise Exception(r.json['error']['code'], r.json['error']['message'])

	## Remove Folder
	def rmdir(self, path):
		if(self.debug):
			print("[Bitcasa] Removing Directory at Path: " + path)
		payload = {'path' : path}
		if(self.debug):
			print("[Network] Request: " + self.bitcasa_api_url + "/folders/?access_token=" + path + "?access_token=" + self.api_access_token)
		r = requests.delete(self.bitcasa_api_url + "/folders/?access_token=" + self.api_access_token, data=payload)
		if(r.status_code == 200):
			if(r.json()['error'] == None):
				# Success
				# @todo - If it doesn't delete anything (if not found) it will still return a success.
				return r.json()['result']
			else:
				raise Exception(r.json()['error']['code'], r.json()['error']['message'])
		else:
			raise Exception(r.json['error']['code'], r.json['error']['message'])

	## Rename Folder
	def renamedir(self, path, new_name):
		if(self.debug):
			print("[Bitcasa] Renaming Directory With Path: " + path + " To: " + new_name)
		payload = {'from' : path, 'filename': new_name}
		if(self.debug):
			print("[Network] Request: " + self.bitcasa_api_url + "/folders?operation=rename&access_token=" + self.api_access_token)
		r = requests.post(self.bitcasa_api_url + "/folders?operation=rename&access_token=" + self.api_access_token, data=payload)
		if(r.status_code == 200):
			if(r.json()['error'] == None):
				# Success
				# @todo - If it doesn't delete anything (if not found) it will still return a success.
				return r.json()['result']
			else:
				raise Exception(r.json()['error']['code'], r.json()['error']['message'])
		else:
			raise Exception(r.json['error']['code'], r.json['error']['message'])

	## Move Folder
	def mvdir(self, path, new_path):
		payload = {'from' : path, 'to': new_path}
		r = requests.post(self.api_url + "/folders?operation=move&access_token=" + self.access_token, data=payload)
		if(r.status_code == 200):
			if(r.json()['error'] == None):
				# Success
				# @todo - If it doesn't delete anything (if not found) it will still return a success.
				return True
			else:
				if(r.json()['error']['code'] == 2022):
					raise Exception(2022, r.json()['error']['message'])
				elif(r.json()['error']['code'] == 2023):
					raise Exception(2023, r.json()['error']['message'])
				else:
					# Other Error
					raise Exception("A strange error has occurred. Derp.")
		else:
			if(r.json()['error'] != None):
				raise Exception(r.json()['error']['code'], r.json()['error']['message'])
			else:
				# Other Error
				raise Exception("A strange error has occurred. Derp.")

	## Copy Folder
	def cpdir(self, path, new_path):
		payload = {'from' : path, 'to': new_path}
		r = requests.post(self.api_url + "/folders?operation=copy&access_token=" + self.access_token, data=payload)
		if(r.status_code == 200):
			if(r.json()['error'] == None):
				# Success
				# @todo - If it doesn't delete anything (if not found) it will still return a success.
				return True
			else:
				if(r.json()['error']['code'] == 2022):
					raise Exception(2022, r.json()['error']['message'])
				elif(r.json()['error']['code'] == 2023):
					raise Exception(2023, r.json()['error']['message'])
				else:
					# Other Error
					raise Exception("A strange error has occurred. Derp.")
		else:
			if(r.json()['error'] != None):
				raise Exception(r.json()['error']['code'], r.json()['error']['message'])
			else:
				# Other Error
				raise Exception("A strange error has occurred. Derp.")
	
	### File Methods ###

	## Download File
	def read(self, path, file_id, file_name, file_size, stream=False):
		return False
	
	## Upload File
	# Please Bitcasa, make Uploads better (eh I suppose it works, but it'd be nice to have pause/resume support via chunked requests)
	# Below is a memory efficient, multipart encoding beast.
	# @todo - Maybe add option to send File object directly
	# @todo - Fix content type detection
	def write(self, path, file_path):
		payload = BitcasaUploader(file_path, 8192)
		headers = {'Content-Type': payload.content_type, 'Content-Length': str(payload.totalsize)}
		print(path)
		r = requests.post(self.file_api_url + "/files"+path+"?access_token=" + self.access_token, data=payload, headers=headers);
		print(r.text)
