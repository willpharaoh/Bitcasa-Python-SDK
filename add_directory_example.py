# Bitcasa Add Directory Example #
# 2014 Michael Thomas (Biscuit Labs) #

# Get our Bitcasa Module
from bitcasa import Bitcasa

# Create an instance of the Bitcasa Class
client = Bitcasa('APP_CLIENT_ID','APP_CLIENT_SECRET',True, None, 'ACCESS_TOKEN')

# Get Root Directory Contents
root_dir = client.dir();

# Print Results
i = 0
for files in root_dir:
	print("["+str(i)+"] "+files['name'] + " - " + files['path'])
	i = i + 1

# Get Some User Input
directory = input("Enter Folder number to add New Folder to: ")
folder_name = input("Enter Name for new Folder: ")

# Add Directory
print(client.mkdir(root_dir[int(directory)]['path'], folder_name))
