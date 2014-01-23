# Bitcasa List Directory Example #
# 2013 Michael Thomas (Biscuit Labs) #

# Get our Bitcasa Module
from bitcasa import Bitcasa

# Create an instance of the Bitcasa Class
client = Bitcasa('APP_CLIENT_ID','APP_CLIENT_SECRET',True, None, 'ACCESS_TOKEN')

# Get Root Directory Contents
root_dir = client.dir();

# Print Results
for files in root_dir:
	print(files['name'] + " - " + files['path'])
