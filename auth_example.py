# Bitcasa Authentication Example #
# 2013 Michael Thomas (Biscuit Labs) #

# Get our Bitcasa Module
from bitcasa import Bitcasa

# Create an instance of the Bitcasa Class
client = Bitcasa('APP_CLIENT_ID','APP_CLIENT_SECRET',True)

# Get our URL
print("Bitcasa OAuth URL: " + client.oauth_url())

# Get Auth Code
print("Now, go to the URL above in a Web Browser and Enter the Authorization Code Below")
auth_code = input("Authorization Code: ")

# Authenticate
print("Your access token: " + client.authenticate(auth_code))
