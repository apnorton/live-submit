##
# submit.py
# 
# The primary submission file.  This handles UI and web interfacing.
##

from getpass import getpass
from connection import LAConnection 
    
##
# Get username and password
# (currently from user, possibly later from file)
##
def get_credentials():
  username = input("Username: ")
  password = getpass("Password: ")

  return username, password

if __name__=='__main__':
  print("     live-submit     (v0.1)")

  # Set up the connection
  uname, pword = get_credentials()
  jc = LAConnection(uname, pword)

