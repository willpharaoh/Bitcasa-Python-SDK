# Bitcasa User Profile Example #
# 2014 Michael Thomas (Biscuit Labs) #

# Get our Bitcasa Module
from bitcasa import Bitcasa

# Create an instance of the Bitcasa Class
client = Bitcasa('APP_CLIENT_ID','APP_CLIENT_SECRET',True, None, 'ACCESS_TOKEN')

# Get & Print User Profile
print(client.user_profile());
