# Bitcasa Download File Example #
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
file_num = input("Enter # of File to Download: ")
new_name = input("Input Filename to Save File As: ")

# Download File (by path)
with open(new_name, 'wb') as file:
	file.write(client.download(dir_contents[int(file_num)]['path'],None, new_name))
