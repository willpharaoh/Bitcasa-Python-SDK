# Unofficial Bitcasa Python SDK

#### A quick and dirty Python SDK for Bitcasa. Unofficial, of course.

### Features
* Authentication (get OAuth URL & API Access Token from OAuth Token)
* Get User Profile
* List a Directory
* Create a Directory
* Delete a Directory
* Rename a Directory
* Download a File
* Upload a File

(each of the above features include a fully working example).

### Installation & Requirements
##### The following has been tested on Ubuntu 13.04.
1. Ensure you have Python 3 & Requests (http://docs.python-requests.org/)
    2. On Ubuntu 13.04, you can accomplish this by doing:

    ``` sudo apt-get install python3-pip && sudo pip3 install requests```
2. Next, go to https://developer.bitcasa.com/ and get a Client Key and Client Secret from the Console.
3. Download the SDK and play with the examples - they're commented decently and all work.
