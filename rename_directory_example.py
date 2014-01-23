# Bitcasa Rename Directory Example #
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
directory = input("Enter # of Folder to Enter: ")
dir_contents = client.dir(root_dir[int(directory)]['path'])

# Enter Directory & Print Results
i = 0
for files in dir_contents:
	print("["+str(i)+"] "+files['name'] + " - " + files['path'])
	i = i + 1

# Get More User Input
rename_dir = input("Enter # of Folder to Rename: ")
new_name = input("Input New Folder Name: ")

# Rename Directory
print(client.renamedir(dir_contents[int(rename_dir)]['path'],new_name))
