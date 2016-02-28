import requests
from bs4 import BeautifulSoup

##
# This object acts as an interface to the live archive
##
class LAConnection:
  archive_url  = 'https://icpcarchive.ecs.baylor.edu/index.php'
  login_form   = '?option=com_comprofiler&task=login'
  submit_form  = '?option=com_onlinejudge&Itemid=25'
  submit_dest  = 'index.php?option=com_onlinejudge&Itemid=25&page=save_submission'

  # values from submit_form radio buttons
  language_map = { 
                   'c'      : 1,
                   'java'   : 2,
                   'c++'    : 3,
                   'pascal' : 4,
                   'c++11'  : 5,
                   'pyth'   : 6
                 }

  ##
  # LAConnection(uname : string, pword : string)
  # Creates an LAConnection with a given username and password
  ##
  def __init__(self, uname, pword):
    self.uname   = uname
    self.pword   = pword
    self.session = requests.Session()

    # Perform the login request
    self.login()

  ##
  # is_connected()
  # Checks if we're logged in to live archive
  ##
  def is_connected(self):
    s = self.session
    homepage = s.get(self.archive_url)
    soup = BeautifulSoup(homepage.text, 'html.parser')

    greetings = soup.findAll(id='mod_login_greeting')

    return len(greetings) > 0 
    
  ##
  # login()
  # Performs a login based on username/password attributes
  ##
  def login(self):
    s = self.session
    print('Performing login...')

    # Get data from login page to spoof being a real user
    homepage = s.get(self.archive_url)
    soup = BeautifulSoup(homepage.text, 'html.parser')
    hiddenInputs = soup.findAll(name='input', type='hidden')

    payload = { 'username':self.uname, 'passwd':self.pword, 'remember':'yes' }
    for hidden in hiddenInputs:
      if hidden['name'] != 'option' and hidden['value'] != 'search':
        payload[hidden['name']] = hidden['value']

    headers = { 'User-Agent':'Mozilla/5.0', 'Referrer':'https://icpcarchive.ecs.baylor.edu/index.php' }
    self.session.post(LAConnection.archive_url+LAConnection.login_form, data=payload).text

    if self.is_connected():
      print('Login complete.')
    else:
      # TODO make an actual exception class for this purpose
      raise Exception('badness occurred on login')
  
  ##
  # upload_code()
  # Given filename and problem ID, perform a submission.
  #
  # filename : a string specifying the relative path to the solution file
  # pid      : a string consisting of an integer specifying the problem id
  # language : a string specifying the language choice
  # TODO Determine why this method isn't producing any effect on the
  #      server. It's as if nothing happens
  ##
  def upload_code(self, pid, filename, language='java'):
    values = {
            'localid' : pid, 'problemid':'', 'category':'',
            'language': self.language_map[language]
           }
     
    files = { 'file' : open(filename, 'rb') }

    requests.post(self.archive_url + self.submit_dest,
                  files = files, params = values)
